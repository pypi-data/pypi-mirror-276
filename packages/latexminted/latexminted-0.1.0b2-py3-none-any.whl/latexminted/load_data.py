# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the LaTeX Project Public License version 1.3c:
# https://www.latex-project.org/lppl.txt
#


from __future__ import annotations

from typing import Any
from .messages import Messages
from .restricted import latex2pydata_loads, RestrictedPath, tempfiledir_path




def load_data(*, md5: str, messages: Messages, timestamp: str, command: str) -> list[dict[str, Any]] | dict[str, Any] | None:
    data_file_name: str = f'_{md5}.data.minted'
    data_path: RestrictedPath = tempfiledir_path / data_file_name

    data_text: str
    try:
        data_text = data_path.read_text()
    except FileNotFoundError:
        messages.append_error(rf'Failed to find file \detokenize{{"{data_file_name}"}}')
        messages.data_file_not_found = True
    except PermissionError:
        messages.append_error(rf'Insufficient permission to open file \detokenize{{"{data_file_name}"}}')
    except UnicodeDecodeError:
        messages.append_error(rf'Failed to decode file \detokenize{{"{data_file_name}"}} (expected UTF-8)')
    if messages.has_errors():
        return None

    try:
        data = latex2pydata_loads(data_text, schema={'cachefiles': 'list[str]'}, schema_missing='rawstr')
    except Exception as e:
        messages.append_error(
            rf'Failed to load data from file \detokenize{{"{data_file_name}"}} (see \detokenize{{"{messages.errlog_file_name}"}})'
        )
        messages.append_errlog(e)
        return None
    if isinstance(data, dict):
        if command != data['command']:
            messages.append_error(
                rf'''minted data file \detokenize{{"{data_file_name}"}} is for "{data['command']}", but expected "{command}"'''
            )
            return None
        if timestamp != data['timestamp']:
            messages.append_error(
                rf'minted data file \detokenize{{"{data_file_name}"}} has incorrect timestamp'
            )
            return None
    elif isinstance(data, list):
        if command != 'batch':
            messages.append_error(
                rf'''minted data file \detokenize{{"{data_file_name}"}} is for "batch", but expected "{command}"'''
            )
            return None
        valid_commands = set(['styledef', 'highlight', 'clean'])
        if not all(d['command'] in valid_commands for d in data):
            messages.append_error(
                rf'''minted data file \detokenize{{"{data_file_name}"}} is for "batch", but contains invalid data'''
            )
            return None
        if data and timestamp != data[0]['timestamp']:
            messages.append_error(
                rf'minted data file \detokenize{{"{data_file_name}"}} has incorrect timestamp'
            )
            return None
    else:
        messages.append_error(
            rf'minted data file \detokenize{{"{data_file_name}"}} contains unexpected data type "{type(data)}"'
        )
        return None
    return data
