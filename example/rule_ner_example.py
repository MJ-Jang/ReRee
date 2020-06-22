from reree.entity_extractor import ReReeExtractor
from reree.helper import get_regex_data, get_regex_combination


# reg_pattern = get_regex_data('data/regex.md')
# comb_pattern = get_regex_combination('data/regex_combination.yml')


extractor = ReReeExtractor()
a = extractor.process("일월 해 줘")
a