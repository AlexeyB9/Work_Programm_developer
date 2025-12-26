# docx_generator.py

from __future__ import annotations

from typing import Iterable, Union, Tuple
import re
from docxtpl import DocxTemplate  # pip install docxtpl


_KEY_CLEAN_RE = re.compile(r"^\s*\{\{\s*|\s*\}\}\s*$")


def _parse_pairs_from_text(text: str) -> list[tuple[str, str]]:
    """
    Превращает ответ вида:
      "ключ:значение; ключ2:значение2; ..."
    (или с переносами строк/пояснениями) в список (key, value).

    Важно: values могут содержать двоеточия, поэтому split делаем только по первому ':'.
    """
    if not text:
        return []

    text = text.replace("\r\n", "\n").strip()

    # Часто модель добавляет пояснение перед парами. Мы просто фильтруем строки/фрагменты без ':'
    # и режем по ';' (если их нет — по переводам строк).
    parts = text.split(";") if ";" in text else text.split("\n")

    pairs: list[tuple[str, str]] = []
    for part in parts:
        part = part.strip()
        if not part or ":" not in part:
            continue
        key, value = part.split(":", 1)
        key = _KEY_CLEAN_RE.sub("", key).strip()
        value = value.strip()
        if key:
            pairs.append((key, value))
    return pairs


def generate_docx_from_template(
    data: Union[str, Iterable[Union[str, Tuple[str, str]]], dict],
    template_path: str,
    output_path: str,
    all_variables: dict[str, str] | None = None,
) -> None:
    """
    data:
        - либо строка (ответ ИИ) вида "key:value; key2:value2; ..."
        - либо список строк вида "key:value"
        - либо список кортежей ("key", "value")
        - либо словарь {"key": "value", ...}
    template_path:
        путь к docx-шаблону (с плейсхолдерами {{ key }})
    output_path:
        путь, куда сохранить сгенерированный docx
    all_variables:
        словарь со всеми переменными из шаблона (для поддержки условных блоков {% if переменная %})
        Если передан, все переменные из этого словаря будут добавлены в контекст, даже если пустые
    """
    context = {}
    
    # Если передан словарь all_variables, добавляем все переменные в контекст
    # Это нужно для работы условных блоков {% if переменная %}
    if all_variables:
        context.update(all_variables)
    
    # Обрабатываем data для добавления/обновления значений переменных
    if isinstance(data, dict):
        # Если data - словарь, просто обновляем контекст
        for key, value in data.items():
            key = str(key).strip()
            if key:
                context[key] = str(value).strip() if value else ""
    elif isinstance(data, str):
        data_iter: Iterable[Union[str, Tuple[str, str]]] = _parse_pairs_from_text(data)
        for item in data_iter:
            if isinstance(item, str):
                item = item.strip()
                if not item or ":" not in item:
                    continue
                key, value = item.split(":", 1)
            else:
                if len(item) != 2:
                    continue
                key, value = item
            
            key = str(key).strip()
            value = str(value).strip()
            if key:
                context[key] = value
    else:
        # Список кортежей или строк
        for item in data:
            if isinstance(item, str):
                item = item.strip()
                if not item or ":" not in item:
                    continue
                key, value = item.split(":", 1)
            else:
                if len(item) != 2:
                    continue
                key, value = item
            
            key = str(key).strip()
            value = str(value).strip()
            if key:
                context[key] = value
    
    doc = DocxTemplate(template_path)
    doc.render(context)
    doc.save(output_path)

