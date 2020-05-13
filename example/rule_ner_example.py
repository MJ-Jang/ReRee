from reree.entity_extractor import ReReeExtractor
from reree.helper import get_regex_data, get_regex_combination


reg_pattern = get_regex_data('data/regex.md')
comb_pattern = get_regex_combination('data/regex_combination.yml')


extractor = ReReeExtractor(reg_pattern, comb_pattern)
extractor.process('다음주 수요일부터 월요일일까지')