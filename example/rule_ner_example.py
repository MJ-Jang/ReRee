from reree.entity_extractor import ReReeExtractor
from reree.helper import get_regex_data, get_regex_combination


reg_pattern = get_regex_data('data/regex.md')
comb_pattern = get_regex_combination('data/regex_combination.yml')


extractor = ReReeExtractor()
a = extractor.process('다음 달 1일을 시작일자로 해서 이주일 동안 로밍 요금제 쓸게요')


