from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TableFillSpec:
    """
    Описание того, как заполнять одну таблицу в docx.
    """

    table_index: int          # индекс таблицы в docx (doc.tables[table_index])
    cols_per_row: int         # сколько колонок заполняем (ширина полезной области)
    start_row: int            # с какой строки начинать (например 1, если 0-я строка — заголовок)
    start_col: int            # с какой колонки начинать
    prompt_idx: int           # индекс промпта в table_prompts.TABLE_PROMPTS


"""
ГДЕ ЗАПОЛНЯТЬ ОСТАЛЬНЫЕ СПИСКИ/НАСТРОЙКИ:

Заполняйте `TABLE_SPECS` в ЭТОМ файле (tables_config.py).
Это заменяет "несколько параллельных массивов" (индексы, колонки, координаты, промпты)
на один список структур, чтобы не перепутать порядок.

Пример: если нужно заполнить 3 таблицы:
    - таблицу 6 (3 колонки, начать с 1:0, промпт 0)
    - таблицу 10 (4 колонки, начать с 2:0, промпт 1)
    - таблицу 12 (2 колонки, начать с 1:0, промпт 2)
"""

TABLE_SPECS: list[TableFillSpec] = [
    # TODO: замените table_index на реальные индексы таблиц вашего result.docx
    TableFillSpec(table_index=1, cols_per_row=3, start_row=1, start_col=0, prompt_idx=0),
    TableFillSpec(table_index=2, cols_per_row=2, start_row=2, start_col=1, prompt_idx=1),
    TableFillSpec(table_index=3, cols_per_row=6, start_row=1, start_col=0, prompt_idx=2),
    TableFillSpec(table_index=4, cols_per_row=2, start_row=1, start_col=0, prompt_idx=3),
    TableFillSpec(table_index=5, cols_per_row=6, start_row=1, start_col=0, prompt_idx=4),
    TableFillSpec(table_index=6, cols_per_row=5, start_row=1, start_col=0, prompt_idx=5),
    TableFillSpec(table_index=7, cols_per_row=3, start_row=1, start_col=0, prompt_idx=6),
    TableFillSpec(table_index=8, cols_per_row=3, start_row=1, start_col=0, prompt_idx=7),
    TableFillSpec(table_index=9, cols_per_row=2, start_row=1, start_col=0, prompt_idx=8),
    TableFillSpec(table_index=10, cols_per_row=2, start_row=1, start_col=0, prompt_idx=9),
    TableFillSpec(table_index=11, cols_per_row=2, start_row=1, start_col=0, prompt_idx=10),
    TableFillSpec(table_index=12, cols_per_row=3, start_row=1, start_col=0, prompt_idx=11),
    TableFillSpec(table_index=15, cols_per_row=3, start_row=1, start_col=0, prompt_idx=12),
    TableFillSpec(table_index=16, cols_per_row=3, start_row=1, start_col=0, prompt_idx=13),
    TableFillSpec(table_index=17, cols_per_row=2, start_row=1, start_col=0, prompt_idx=14),
    TableFillSpec(table_index=18, cols_per_row=2, start_row=1, start_col=0, prompt_idx=15),
    TableFillSpec(table_index=21, cols_per_row=2, start_row=1, start_col=0, prompt_idx=16)
]

# Если ваша нумерация table_index начинается с 1 по "таблицам отчёта" (без служебных таблиц в начале документа),
# задайте смещение сюда.
# Например, если первая "нужная" таблица в docx имеет индекс 5 (0-based) / 6 (1-based docx),
# то TABLE_INDEX_OFFSET = 5.
TABLE_INDEX_OFFSET: int = 5

