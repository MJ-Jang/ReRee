#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division
from typing import Text


def get_regex_data(regex_path: Text):
    with open(regex_path, "r", encoding="utf-8") as nluFile:
        nlu = nluFile.read()
    nlu = [s for s in nlu.split("\n") if s]

    regex_list = []
    for i, s in enumerate(nlu):
        if s.startswith("## regex"):
            name = s.split(":")[-1].strip()
            pattern = nlu[i + 1][1:].strip()
            regex_list.append({"name": name, "pattern": pattern})
    return regex_list
