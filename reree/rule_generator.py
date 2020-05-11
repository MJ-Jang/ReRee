from itertools import product


class RegexPatternGenerator:
    """
    Generate rule consists of the combination of regex patterns

    Usage:
        1) write regex pattern in rule.md file
        2) write combination pattern in combination.yml file
    """

    def __init__(self, regex_data, comb_pattern):
        self.regex_data = {}
        for s in regex_data:
            self.regex_data[s['name']] = s['pattern']
        self.com_pattern = comb_pattern

    def generate_patterns(self):
        outp = []
        for entity in self.com_pattern.keys():
            entity_list = self.com_pattern[entity]
            for e in entity_list:
                if len(e) == 1:
                    outp_ = self.process_single_pattern(e)
                    outp.append(outp_)
                elif len(e) > 1:
                    outp_ = self.process_non_single_pattern(entity, e)
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
            pattern_ += '\\s?'.join(s) + '|'
        outp = {'name': entity_name_, 'pattern': pattern_[:-1]}
        return outp