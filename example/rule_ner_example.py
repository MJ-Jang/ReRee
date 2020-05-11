from reree.entity_extractor import ReReeExtractor
from reree.helper import get_regex_data, get_regex_combination


reg_pattern = get_regex_data('data/rule.md')
comb_pattern = get_regex_combination('data/combination.yml')


extractor = ReReeExtractor(reg_pattern, comb_pattern)
extractor.process('10 GB 충전할라고 했는데 5GB만 충전할래')
