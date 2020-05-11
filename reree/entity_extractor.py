#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division
from reree.time_converter import extract_dates, extract_dates_from_to
from reree.rule_generator import RegexPatternGenerator
from reree.rules import regex_rules

from typing import Text, List, Any

import re


class ReReeExtractor:

    name = "ReReeExtractor"

    def __init__(self, patterns: list) -> None:
        """
        patterns: new list of patterns: [{"name": "City", "pattern": "-1-1-23-9"}, ...]
        """
        super(ReReeExtractor, self).__init__()
        generator = RegexPatternGenerator(patterns)
        self.patterns = generator.generate_patterns()

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
                    extracted.append(entity)
                    text = text[:s] + '#'*(e-s) + text[e:]
        return extracted

    def process(self, text: Text, **kwargs: Any) -> List:
        """Process an incoming message."""
        # match regex entities
        extracted = []
        extracted += self.match_regex(text)

        return extracted
