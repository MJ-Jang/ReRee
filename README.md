## ReRee: Regex Rule Entity Extractor
Reree is a rule based entity extractor for Korean language

### 1) Supporting functions
- Single regex entity extracting
- Combined regex entity extracting
- Time converting

### 2) Usage
##### 1. Install
```
python setup.py install
```

##### 2. Register regex entity in regex.md file
```markdown
## regex:PhoneNumber
- 010[\s\.\-]?\d{3,4}[\s\.\-]?\d{4}
```

##### 3. Regixter regex combination rule in regex_combination.yml file
```yaml
Relative_Date_Past:
  pattern1:
    - Count_Date
    - Time_before
```

##### 4. Load module and process text
```python
from reree.entity_extractor import ReReeExtractor
from reree.helper import get_regex_data, get_regex_combination

reg_pattern = get_regex_data('regex.md')
comb_pattern = get_regex_combination('regex_combination.yml')


extractor = ReReeExtractor(reg_pattern, comb_pattern)
extractor.process('오늘부터 3박4일동안 여행간다')
```