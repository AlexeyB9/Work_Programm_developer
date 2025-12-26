"""
Скрипт для извлечения таблиц из шаблона docx файла.
Для каждой таблицы формируется JSON с информацией о ней и настройками.
Результат сохраняется в JSON файл для отправки на frontend.
"""

import json
from pathlib import Path
from docx import Document


def extract_tables_from_docx(template_path: str) -> list[dict]:
    """
    Извлекает все таблицы из docx файла вместе со всем содержимым.
    
    Args:
        template_path: путь к файлу шаблона
        
    Returns:
        список словарей с информацией о таблицах
    """
    try:
        doc = Document(template_path)
        tables_info = []
        table_counter = 1  # Счетчик для порядкового номера таблиц после фильтрации
        
        # Проходим по всем таблицам в документе
        for table_index, table in enumerate(doc.tables):
            # Получаем информацию о таблице
            num_rows = len(table.rows)
            num_cols = len(table.rows[0].cells) if num_rows > 0 else 0
            
            # Пропускаем таблицы с 1 столбцом, которые содержат только служебный текст (поля для Word)
            # Например, таблицы с текстом "(должность, уч. степень, звание)", "(инициалы, фамилия)" и т.д.
            if num_cols == 1:
                service_patterns = ["(должность", "(инициалы", "(подпись", "«___", "___»", "20__ г"]
                service_keywords = ["утверждаю", "руководитель образовательной программы"]
                
                # Проверяем все ячейки таблицы - если все содержат только служебный текст - пропускаем
                has_real_content = False
                for row in table.rows:
                    for cell in row.cells:
                        cell_text = cell.text.strip()
                        if not cell_text:
                            continue
                        
                        cell_lower = cell_text.lower()
                        
                        # Проверяем, является ли содержимое служебным
                        is_service_cell = (
                            cell_text.startswith("(") or  # Текст в скобках
                            any(pattern in cell_text for pattern in service_patterns) or  # Служебные паттерны
                            cell_lower in service_keywords or  # Служебные ключевые слова
                            ("{{" in cell_text and "}}" in cell_text)  # Переменные тоже считаем служебными для одностолбцовых таблиц
                        )
                        
                        # Если ячейка НЕ служебная - значит это реальная таблица с данными
                        if not is_service_cell:
                            has_real_content = True
                            break
                    
                    if has_real_content:
                        break
                
                # Если нет реального контента (только служебный текст) - пропускаем таблицу
                if not has_real_content:
                    continue
            
            # Извлекаем все данные из таблицы (все строки и столбцы)
            table_data = []
            for row in table.rows:
                row_data = []
                for cell in row.cells:
                    # Извлекаем текст из ячейки (сохраняем как есть, со всеми пробелами)
                    cell_text = cell.text.strip()
                    row_data.append(cell_text)
                table_data.append(row_data)
            
            # Формируем описание таблицы
            table_info = {
                "table_index": table_index,  # 0-based индекс (как в python-docx, реальный индекс в документе)
                "table_number": table_counter,  # Порядковый номер после фильтрации (1-based)
                "name": "",  # Название таблицы (заполняется вручную)
                "num_rows": num_rows,
                "num_cols": num_cols,
                "data": table_data,  # Все данные таблицы (массив строк, каждая строка - массив ячеек)
                "can_add_rows": False,  # По умолчанию нельзя добавлять строки
                "should_fill_with_ai": False  # По умолчанию не заполнять с помощью ИИ
            }
            
            tables_info.append(table_info)
            table_counter += 1
        
        return tables_info
        
    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла {template_path}: {e}")


def main():
    """Главная функция для извлечения таблиц и сохранения в JSON"""
    # Путь к шаблону (относительно корня проекта)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    template_path = project_root / "files" / "Шаблон.docx"
    
    if not template_path.exists():
        print(f"Ошибка: файл {template_path} не найден!")
        return
    
    print(f"Чтение файла: {template_path}")
    
    # Извлекаем таблицы
    tables = extract_tables_from_docx(str(template_path))
    
    print(f"Найдено таблиц: {len(tables)}")
    
    # Формируем JSON структуру
    result = {
        "tables": tables,
        "count": len(tables)
    }
    
    # Сохраняем в JSON файл (в корне проекта)
    output_path = project_root / "template_tables.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Результат сохранен в: {output_path}")
    print("\nСписок найденных таблиц:")
    for i, table in enumerate(tables, 1):
        name = table['name'] if table['name'] else "(без названия)"
        print(f"  {i}. Таблица #{table['table_number']} (индекс {table['table_index']}): {name} - "
              f"{table['num_rows']} строк, {table['num_cols']} колонок")
        # Показываем превью первой строки
        if table['data'] and len(table['data']) > 0:
            first_row_preview = " | ".join([cell[:30] for cell in table['data'][0][:3] if cell])
            if len(table['data'][0]) > 3:
                first_row_preview += "..."
            print(f"     Первая строка: {first_row_preview}")


if __name__ == "__main__":
    main()

