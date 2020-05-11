#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division
from reree.rule_generator import RegexPatternGenerator

from typing import Text, List, Any

import re


class ReReeExtractor:

    name = "ReReeExtractor"

    def __init__(self, regex_patterns: list, combination_patterns: dict) -> None:
        """
        patterns: new list of patterns: [{"name": "City", "pattern": "-1-1-23-9"}, ...]
        """
        super(ReReeExtractor, self).__init__()
        generator = RegexPatternGenerator(regex_patterns, combination_patterns)
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
