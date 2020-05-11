from reree.entity_extractor import ReReeExtractor
from reree.helper import get_regex_data


reg_pattern = get_regex_data('reree/data/rule.md')


extractor = ReReeExtractor(reg_pattern)
extractor.process('10GB 충전할라고 했는데 5GB만 충전할래')
