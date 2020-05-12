## regex:Email
- [\w\.\-]+@[\w]+\.com|[\w\.\-]+@[\w]+\.co.kr

## regex:PhoneNumber
- 010[\s\.\-]?\d{3,4}[\s\.\-]?\d{4}|011[\s\.\-]?\d{3,4}[\s\.\-]?\d{4}

## regex:Data_Units
- 기가|G|GB|기가바이트|메가|메가바이트|M|MB

## regex:Data_Numbers
- [일이삼사오육칠팔구십백천]+|[0-9]{1,4}

## regex:Year
- 19\d{2}년|20\d{2}년

## regex:Count_Year
- [한두세네]\s?해|[일이삼사오육칠팔구십]년|\d{1,2}년

## regex:Relative_Year_Present
- 이번해|올해|금년|당년|본년

## regex:Relative_Year_Future_1
- 다음해|이듬해|내년|명년|담해

## regex:Relative_Year_Future_2
- 다음다음해|다다음해|다담해|후년

## regex:Relative_Year_Past_1
- 지난해|작년|전년

## regex:Relative_Year_Past_2
- 재작년

## regex:Month
- \d{1,2}월달?|[일이삼사오육칠팔구십시유]{1,2}월달?|\d{1,2}月|[첫둘셋넷]째\s?달|[다여]섯째\s?달|[일곱여덟아홉]{1,2}째\s?달|열[한두]?번째\s?달

## regex:Count_Month
- \d{1,2}개월|[일이삼사요육칠팔구십]{1,2}개월|[한둘세네석넉]\s?달|[다여]섯\s?달|[일곱여덟아홉]{1,2}\s?달|열[한두]?\s?달

## regex:Relative_Month_Present
- 요번 달|지금 달|이번 달|이번달|요번달|금월|당월|본월|이달|금달

## regex:Relative_Month_Future_1
- 다음 달|다음달|내달|내월|익월|담달|명월

## regex:Relative_Month_Future_2
- 다다음달|내후 달|내후달|다담달

## regex:Relative_Month_Past_1
- 지난달|저번달|전번달|전월달|작월|전월|전달|객월|거월|작달

## regex:Relative_Month_Past_2
- 지지난달|저저번달|내전 달|전전달|전전월

## regex:Count_Week
- \d{1,2}주일?|[일이삼사오육칠팔구십]{1,2}주일?|[한두세네]\s?주|다섯\s?주

## regex:Week_day
- [월화수목금토일]요일날?|[월화수목금토일]욜|불금|주말|주일

## regex:Relative_Week_Present
- 이번 주|요번 주|이번주|요번주|금주

## regex:Relative_Week_Future_1
- 다음 주|다음주|내주|담주|익주

## regex:Relative_Week_Future_2
- 다다음주|다담주

## regex:Relative_Week_Past_1
- 저번 주|지난 주|저번주|전번주|지난주|작주|전주|거주

## regex:Relative_Week_Past_2
- 지지난주|저저번주|전전주

## regex:Date
- \d{1,2}일날?|[일이삼사오육칠팔구십]{1,2}일날?|\d{1,2}日|1st|2nd|3rd|\d{1,2}th

## regex:Count_Date
- 하루|이틀|사흘|나흘|닷새|엿새|이레|여드레|아흐레|열흘|보름

## regex:Relative_Date_Present
- today|투데이|오늘|금일|지금

## regex:Relative_Date_Future_1
- 다음 날|다음날|내일|명일|담날|일일|낼

## regex:Relative_Date_Future_2
- 내일의 다음날|내일 다음날|내일 모레|내일모레|명후일|날모레|모레

## regex:Relative_Date_Past_1
- yesterday|예스터데이|전일|전날|작일

## regex:Relative_Date_Past_2
- 그저께|어제의|전날|어제

## regex:Time_after
- 이후|후|뒤

## regex:Time_before
- 이전|전

## regex:Period_phrase
- 동안|간

## regex:Period_time
- \d{1,2}박\s?\d{1,2}일

## regex:Date_Format_YMD
- (?:20|19)?\d{2}[\s\.\-/]+[0-1]?\d[\s\.\-/]+[0-3]?\d일?날?

## regex:Date_Format_MB
- [0-1]?\d[\s\.\-/]+[0-3]?\\d일?날?