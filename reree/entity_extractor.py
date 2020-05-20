#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division
from reree.rule_generator import RegexPatternGenerator
from reree.time_converter import extract_dates_from_to
from reree.helper import get_regex_data, get_regex_combination

from typing import Text, List, Any

import re
import os


class ReReeExtractor:

    name = "ReReeExtractor"

    def __init__(self, regex_patterns: list = None, combination_patterns: dict = None, today=None) -> None:
        """
        patterns: new list of patterns: [{"name": "City", "pattern": "-1-1-23-9"}, ...]
        """
        super(ReReeExtractor, self).__init__()

        here = '/'.join(os.path.dirname(__file__).split('/'))
        regex_path = os.path.join(here, "resources", 'regex.md')
        comb_path = os.path.join(here, "resources", 'regex_combination.yml')

        patterns = get_regex_data(regex_path)
        combination = get_regex_combination(comb_path)

        # add inserted patterns
        if regex_patterns:
            for p in regex_patterns:
                if p not in patterns:
                    patterns.append(p)
        # add inserted dict
        if combination_patterns:
            for key, value in combination_patterns.items():
                if not combination.get(key):
                    combination[key] = value

        generator = RegexPatternGenerator(patterns, combination)
        self.patterns = generator.generate_patterns()
        self.today = None

    def process(self, text: Text, **kwargs: Any) -> List:
        """Process an incoming message."""
        # match regex entities
        extracted = []
        extracted += self.match_regex(text)
        extracted = self.remove_overlap(extracted)

        # extract start/end date
        start_end = extract_dates_from_to(text=text, entities=extracted, today=self.today)
        for key in start_end.keys():
            entity = {
                "start": -1,
                "end": -1,
                "value": start_end.get(key),
                "confidence": 1.0,
                "entity": key,
            }
            extracted.append(entity)
        return extracted

    def match_regex(self, text: Text):
        extracted = []
        for d in self.patterns:
            matches = re.findall(pattern=d['pattern'], string=text)
            if matches:
                for pattern_ in matches:
                    match = re.search(pattern=pattern_, string=text)
                    s, e = match.span()
                    entity = {
                        "start": s,
                        "end": e,
                        "value": match.group(),
                        "confidence": 1.0,
                        "entity": d["name"],
                    }
                    if len(matches) > 1:
                        text = text[:s] + '#'*len(match.group()) + text[e:]

                    extracted.append(entity)
        return extracted

    @staticmethod
    def remove_overlap(entity_result):
        def check_range_intersect(inp, tgt):
            if inp[0] == tgt[0] and inp[1] == tgt[1]:
                return False
            else:
                if inp[0] >= tgt[0]:
                    if inp[1] <= tgt[1]:
                        return True
                return False

        pos = [(o['start'], o['end']) for o in entity_result]
        idx = []
        for i in range(len(pos)):
            for j in range(len(pos)):
                if check_range_intersect(pos[i], pos[j]):
                    idx.append(i)
        out = [entity_result[i] for i in range(len(entity_result)) if i not in idx]
        return out
