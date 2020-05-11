from itertools import product


class RegexPatternGenerator:
    """
    Generate rule consists of the combination of regex patterns

    Usage:
        1) write regex pattern in rule.md file
        2) declare entity name as a variable name (ex: regex_{PatternName})
        3) write regex patterns composing the entity in order (ex: regex_{PatternName} = [('Data', 'PhoneNumber')])
    """

    regex_PhoneNumber = [('PhoneNumber',)]
    regex_Email = [('Email',)]
    regex_Data_Size = [('Data_Numbers', 'Data_Units')]

    def __init__(self, regex_data):
        self.patterns = [s for s in RegexPatternGenerator.__dict__.keys() if 'regex' in s]
        self.attribute_dict = RegexPatternGenerator.__dict__
        self.regex_data = {}
        for s in regex_data:
            self.regex_data[s['name']] = s['pattern']

    def generate_patterns(self):
        outp = []
        for p in self.patterns:
            entity_list = self.attribute_dict[p]
            for e in entity_list:
                if len(e) == 1:
                    outp_ = self.process_single_pattern(e)
                    outp.append(outp_)
                elif len(e) > 1:
                    outp_ = self.process_non_single_pattern(p, e)
                    outp.append(outp_)
        return outp

    def process_single_pattern(self, entity_list: list):
        entity_name_ = entity_list[0]
        pattern_ = self.regex_data[entity_name_]
        outp = {'name': entity_name_, 'pattern': pattern_}
        return outp

    def process_non_single_pattern(self, pattern_name: str, entity_list: list):
        entity_name_ = pattern_name.replace('regex_', '')
        order_dict = {}
        for s in entity_list:
            order_dict[s] = sorted(self.regex_data[s].split('|'), key=lambda x: len(x), reverse=True)
        pattern_comb = [order_dict[key] for key in order_dict.keys()]
        pattern_comb = list(product(*pattern_comb))

        pattern_ = ''
        for s in pattern_comb:
            pattern_ += ''.join(s) + '|'
        outp = {'name': entity_name_, 'pattern': pattern_[:-1]}
        return outp
