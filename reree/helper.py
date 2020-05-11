#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division
from typing import Text

import yaml


def get_regex_data(regex_path: Text):
    with open(regex_path, "r", encoding="utf-8") as regexFile:
        regex = regexFile.read()
    regex = [s for s in regex.split("\n") if s]

    regex_list = []
    for i, s in enumerate(regex):
        if s.startswith("## regex"):
            name = s.split(":")[-1].strip()
            pattern = regex[i + 1][1:].strip()
            regex_list.append({"name": name, "pattern": pattern})
    return regex_list


def get_regex_combination(combination_path: Text):
    with open(combination_path, "r", encoding="utf-8") as combFile:
        comb = yaml.safe_load(combFile)

    comb_dict = {}
    for key in comb.keys():
        comb_dict[key] = []
        for key2 in comb[key].keys():
            comb_dict[key].append(comb[key][key2])
    return comb_dict