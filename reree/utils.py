#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division

from reree.patterns import *

import re


def normalize_pattern(value: str, pattern_dict: dict) -> str:
    """
    normalize single value according to the pattern dict
    """

    for k, v in pattern_dict.items():
        pattern = re.compile('|'.join(v))
        res = pattern.search(string=value)
        if res:
            value = pattern.sub(k, value)
            break
    return value


def normalize_Count_time(value: str) -> str:
    """
    normalize time related entity values
    """
    pattern_list = [YEAR_PATTERN, MONTH_PATTERN_STACTIC, MONTH_PATTERN, WEEK_PATTERN, DATE_PATTERN]

    for pattern in pattern_list:
        out = normalize_pattern(value, pattern)
        if out != value:
            return out
    return value
