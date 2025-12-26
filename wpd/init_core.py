"""
Инициализация ядра: обработка файлов через Perplexity API и заполнение шаблона.
"""

from pathlib import Path

from wpd.fill_tables import fill_tables_from_lists
from wpd.merge_with_docx import generate_docx_from_template
from wpd.request_api import call_api_in_one
from wpd.table_prompts import TABLE_PROMPTS
from wpd.tables_config import TABLE_SPECS, TABLE_INDEX_OFFSET


def init_core(
        file1_path: str,
        file2_path: str,
        prompt: str,
        model: str = "sonar",
        template_path: str | None = None,
        result_path: str | None = None,
        skip_tables: bool = False,
) -> tuple[str, str]:
    """
    Основная функция инициализации ядра:
    1. Отправляет два файла и промпт в Perplexity API
    2. Генерирует result.docx из шаблона (пересоздает файл при первом запросе)
    3. Заполняет все таблицы по конфигурации (если skip_tables=False)

    Args:
        file1_path: путь к первому файлу
        file2_path: путь ко второму файлу
        prompt: промпт для обработки файлов
        model: модель Perplexity (по умолчанию "sonar")
        template_path: путь к шаблону DOCX (по умолчанию "files/Шаблон.docx")
        result_path: путь к результирующему файлу DOCX (по умолчанию "files/result.docx")
        skip_tables: если True, пропускает заполнение таблиц по конфигурации
    
    Returns:
        tuple[str, str]: (result_path, thread_id) - путь к результату и thread_id для дальнейшей работы
    """
    # Устанавливаем пути по умолчанию
    if template_path is None:
        template_path = "../files/Шаблон.docx"
    if result_path is None:
        result_path = "files/result.docx"
    # Шаг 1: Отправка запроса в API Perplexity
    print(f"Отправка запроса в API Perplexity (модель: {model})...")
    try:
        answer, thread_id = call_api_in_one(file1_path, file2_path, prompt, model)
        print("\n" + "=" * 50)
        print("Полный ответ API:")
        print("=" * 50)
        print("=" * 50)
    except FileNotFoundError as e:
        error_msg = f"Ошибка: Файл не найден - {e}"
        print(error_msg)
        raise FileNotFoundError(error_msg) from e
    except ValueError as e:
        error_msg = f"Ошибка: {e}"
        print(error_msg)
        raise ValueError(error_msg) from e
    except Exception as e:
        error_msg = f"Ошибка при запросе к API: {e}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        raise Exception(error_msg) from e

    # Шаг 2: Генерация result.docx из шаблона (пересоздает файл)
    # Убеждаемся, что папка files существует
    result_file = Path(result_path)
    result_file.parent.mkdir(parents=True, exist_ok=True)

    # Удаляем старый файл, если существует и он не используется как шаблон
    # Если template_path и result_path одинаковые, значит используем уже созданный файл
    if result_file.exists() and str(template_path) != str(result_path):
        try:
            result_file.unlink()
            print(f"Удален старый файл: {result_path}")
        except PermissionError:
            print(f"Предупреждение: Не удалось удалить старый файл {result_path} (возможно, открыт в Word)")

    generate_docx_from_template(answer, template_path, result_path)
    print(f"Создан файл: {result_path}")

    # Шаг 3: Заполнение всех нужных таблиц в цикле по конфигу (если не пропущено)
    if not skip_tables:
        try:
            table_indices = [s.table_index for s in TABLE_SPECS]
            cols_per_row_list = [s.cols_per_row for s in TABLE_SPECS]
            start_coords = [(s.start_row, s.start_col) for s in TABLE_SPECS]
            prompts = [TABLE_PROMPTS[s.prompt_idx] for s in TABLE_SPECS]

            fill_tables_from_lists(
                result_docx_path=result_path,
                table_indices=table_indices,
                cols_per_row_list=cols_per_row_list,
                start_coords=start_coords,
                prompts=prompts,
                model=model,
                thread_id=thread_id,
                index_base=1,  # table_index в tables_config.py у вас начинается с 1
                table_index_offset=TABLE_INDEX_OFFSET,
            )
            print(f"\nЗаполнение таблиц завершено. Результат сохранен в: {result_path}")
        except Exception as e:
            error_msg = f"Не удалось заполнить таблицы по спискам: {e}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            raise Exception(error_msg) from e
    else:
        print("Пропущено заполнение таблиц по конфигурации (будут обработаны из JSON)")
    
    return (result_path, thread_id)
