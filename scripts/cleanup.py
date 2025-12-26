"""
Скрипт для очистки временных файлов перед развертыванием.
"""

import os
from pathlib import Path

def cleanup():
    """Удаляет временные файлы и результаты"""
    base_dir = Path(__file__).parent.parent
    
    # Список паттернов для удаления
    patterns_to_remove = [
        "files/results/*.docx",
        "files/uploads/*.docx",
        "files/telegram_uploads/*.docx",
        "files/telegram_results/*.docx",
        "__pycache__",
        "*.pyc",
        "result.docx",
        "*.xlsx",
    ]
    
    removed_count = 0
    
    # Удаляем файлы результатов
    for pattern in patterns_to_remove:
        if "*" in pattern:
            # Используем glob
            for path in base_dir.glob(pattern):
                try:
                    if path.is_file():
                        path.unlink()
                        removed_count += 1
                        print(f"✓ Удален: {path}")
                    elif path.is_dir():
                        import shutil
                        shutil.rmtree(path)
                        removed_count += 1
                        print(f"✓ Удалена папка: {path}")
                except Exception as e:
                    print(f"⚠ Не удалось удалить {path}: {e}")
        else:
            path = base_dir / pattern
            if path.exists():
                try:
                    if path.is_file():
                        path.unlink()
                        removed_count += 1
                        print(f"✓ Удален: {path}")
                    elif path.is_dir():
                        import shutil
                        shutil.rmtree(path)
                        removed_count += 1
                        print(f"✓ Удалена папка: {path}")
                except Exception as e:
                    print(f"⚠ Не удалось удалить {path}: {e}")
    
    # Удаляем тестовые файлы (не шаблон)
    test_files = [
        "files/Продвинутый_уровень_*.docx",
        "files/Документ1.docx",
    ]
    
    for pattern in test_files:
        for path in base_dir.glob(pattern):
            try:
                if path.exists() and path.name != "Шаблон.docx":
                    path.unlink()
                    removed_count += 1
                    print(f"✓ Удален тестовый файл: {path}")
            except Exception as e:
                print(f"⚠ Не удалось удалить {path}: {e}")
    
    print(f"\n✅ Очистка завершена. Удалено файлов/папок: {removed_count}")


