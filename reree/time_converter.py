#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division

import datetime
import re
import copy

fmt = '%Y.%m.%d'
date_pattern = re.compile(pattern='20\\d{2}\\.[0-1]\\d\\.[0-3]\\d')
KST = datetime.timezone(datetime.timedelta(hours=9))

days = ['월', '화', '수', '목', '금', '토', '일']

# sequence is important
timeEntityList = [
    {'name': 'Year_P', 'pattern': '19\\d{2}년|20\\d{2}년'},
    {'name': 'Month_P', 'pattern': '1?[0-9]월[달]?'},
    {'name': 'Relative_Month_Future_1', 'pattern': '다음 달|다음달|내달|내월|익월|담달|명월|다음 달'},
    {'name': 'Relative_Month_Present', 'pattern': '요번 달|지금 달|이번 달이번달|금월|당월|본월|이달|금달|요번달'},
    {'name': 'Relative_Week_Future_1', 'pattern': '다음 주|다음주|내주|담주|익주'},
    {'name': 'Relative_Week_Present', 'pattern': '이번 주|요번 주|이번주|요번주|금주'},
    {'name': 'Week_day', 'pattern': '[월화수목금토일]요일날?|[월화수목금토일]욜|불금|주말|주일'},
    {'name': 'Date_P', 'pattern': '[1-3]?[0-9]일[날]?'},
    {'name': 'Relative_Date_Future_2', 'pattern': '내일의 다음날|내일 다음날|내일 모레|내일모레|명후일|날모레|모레'},
    {'name': 'Relative_Date_Future_1', 'pattern': '다음 날|다음날|내일|명일|담날|일일'},
    {'name': 'Relative_Date_Present', 'pattern': 'today|투데이|오늘|금일|지금'},
]

specialMappingDict = {
    "Week_day": {
        '불금': '금요일',
        '주말': '토요일',
        '주일': '일요일'
    }
}


def get_today_date():
    return datetime.datetime.now(tz=KST).strftime(fmt)


def calculate_date_from_period(s_date: str, period: int):
    if date_pattern.match(s_date):
        date = datetime.datetime.strptime(s_date, fmt)
        date += datetime.timedelta(period)
        return date.strftime(fmt)
    else:
        raise ValueError("start date does not match for date type")


def calculate_period_from_date(s_date: str, e_date: str):
    if date_pattern.match(s_date) and date_pattern.match(e_date):
        diff = (datetime.datetime.strptime(e_date, fmt) - datetime.datetime.strptime(s_date, fmt)).days
        return diff
    else:
        raise ValueError("start date does not match for date type")


def is_before_grounddate(input_date: str, ground_date: str):
    if date_pattern.match(ground_date) and date_pattern.match(input_date):
        g_date = datetime.datetime.strptime(ground_date, fmt)
        i_date = datetime.datetime.strptime(input_date, fmt)

        if g_date > i_date:
            return True
        elif g_date < i_date:
            return False
        elif g_date == i_date:
            return 'same'
    else:
        raise ValueError("start date does not match for date type")


# 1. Detect entity
def extract_entities(text: str):
    entities = []
    for pattern in timeEntityList:
        entity = re.findall(pattern=pattern['pattern'], string=text)
        if entity:
            for v in entity:
                s, e = re.search(pattern=v, string=text).span()
                text = text[:s] + '#'*(e-s) + text[e:]
                outp = {
                    "start": s,
                    "end": e,
                    "value": v,
                    "entity": pattern["name"],
                }
                entities.append(outp)
    if entities:
        entities = sorted(entities, key=lambda x: x['start'])
    return entities, text


def check_combination(entities: list):
    outp = []
    if entities[0]['entity'] in ['Date_P', 'Week_day', 'Relative_Date_Present',
                                 'Relative_Date_Future_1', 'Relative_Date_Future_2']:
        tmp = {
            'comb': [entities[0]['entity']],
            str(entities[0]['entity']): entities[0]['value']
        }
        outp.append(tmp)

    for i in range(1, len(entities)):
        # Date_P rule
        if entities[i]['entity'] == 'Date_P':
            if entities[i - 1]['entity'] in ['Month_P', 'Relative_Month_Present',
                                             'Relative_Month_Future_1', 'Relative_Date_Future_2']:
                tmp = {
                    'comb': [entities[i - 1]['entity'], entities[i]['entity']],
                    str(entities[i - 1]['entity']): entities[i - 1]['value'],
                    str(entities[i]['entity']): entities[i]['value'],
                }
                outp.append(tmp)
            else:
                tmp = {
                    'comb': [entities[i]['entity']],
                    str(entities[i]['entity']): entities[i]['value']
                }
                outp.append(tmp)
        # Week day Rule
        elif entities[i]['entity'] == 'Week_day':
            if entities[i - 1]['entity'] in ['Relative_Week_Present', 'Relative_Week_Future_1']:
                tmp = {
                    'comb': [entities[i - 1]['entity'], entities[i]['entity']],
                    str(entities[i - 1]['entity']): entities[i - 1]['value'],
                    str(entities[i]['entity']): entities[i]['value'],
                }
                outp.append(tmp)

            else:
                tmp = {
                    'comb': [entities[i]['entity']],
                    str(entities[i]['entity']): entities[i]['value']
                }
                outp.append(tmp)

        elif entities[i]['entity'] in ['Relative_Date_Present',
                                       'Relative_Date_Future_1', 'Relative_Date_Future_2']:
            tmp = {
                'comb': [entities[i]['entity']],
                str(entities[i]['entity']): entities[i]['value']
            }
            outp.append(tmp)
    return outp


def transform_weekday(value: str) -> str:
    if value in specialMappingDict['Week_day']:
        value = specialMappingDict['Week_day'][value]
    return value[0]


def convert_to_date(cand: dict, today=None) -> str:

    def set_date(year: int, month: int, day: int):
        date = ''
        try:
            date = datetime.date(year=year, month=month, day=day)
            return date
        except ValueError:
            return date

    if not today:
        today = datetime.datetime.now(tz=KST)

    date = ''

    if cand['comb'] == ['Relative_Date_Present']:
        date = today

    if cand['comb'] == ['Relative_Date_Future_1']:
        date = today + datetime.timedelta(days=1)

    if cand['comb'] == ['Relative_Date_Future_2']:
        date = today + datetime.timedelta(days=2)

    if cand['comb'] == ['Date_P']:
        day = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Date_P']))
        date = set_date(year=today.year, month=today.month, day=day)

    if cand['comb'] == ['Month_P', 'Date_P']:
        month = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Month_P']))
        day = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Date_P']))
        date = set_date(year=today.year, month=month, day=day)

    if cand['comb'] == ['Relative_Month_Present', 'Date_P']:
        day = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Date_P']))
        date = set_date(year=today.year, month=today.month, day=day)

    if cand['comb'] == ['Relative_Month_Future_1', 'Date_P']:
        day = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Date_P']))
        date = set_date(year=today.year, month=today.month + 1, day=day)

    if cand['comb'] == ['Week_day']:
        day = transform_weekday(cand['Week_day'])
        today_day = days[today.weekday()]

        diff = days.index(day) - days.index(today_day)
        date = today + datetime.timedelta(days=diff)

    if cand['comb'] == ['Relative_Week_Present', 'Week_day']:
        day = transform_weekday(cand['Week_day'])
        today_day = days[datetime.datetime.today().weekday()]
        diff = days.index(day) - days.index(today_day)
        date = today + datetime.timedelta(days=diff)

    if cand['comb'] == ['Relative_Week_Future_1', 'Week_day']:
        day = transform_weekday(cand['Week_day'])
        today_day = days[datetime.datetime.today().weekday()]
        diff = days.index(day) - days.index(today_day)
        date = today + datetime.timedelta(days=7 + diff)

    if date:
        return date.strftime(fmt)
    else:
        return []


def get_regex_date(text: str, today=None):
    if not today:
        today = datetime.datetime.now(tz=KST)

    p_ymd = re.compile('\\d{2,4}[\\s\\.-/]+[0-1]?\\d[\\s\\.-/]+[0-3]?\\d일?날?') # y-m-d
    p_md = re.compile('[0-1]?\\d[\\s\\.-/]+[0-3]?\\d일?날?') # m-d

    outp = []

    ymd = p_ymd.findall(text)
    if ymd:
        for d in ymd:
            try:

                year, month, day = [int(s.strip()) for s in re.split(pattern='[\\s\\.-/]+', string=d)]
                if len(str(year)) == 2:
                    year = int(str(today.year)[:2] + str(year))
                date = datetime.date(year=year, month=month, day=day).strftime(fmt)
                outp.append(date)
                text = text.replace(d, '#' * len(d))
            except ValueError:
                logger.info('Specified year/month/day cannot be transformed to date')

    md = p_md.findall(text)
    if md:
        for d in md:
            try:
                month, day = [int(re.sub(pattern='[^\\d]+', repl='', string=s).strip())
                              for s in re.split(pattern='[\\s\\.-/]+', string=d)]
                date = datetime.date(year=today.year, month=month, day=day).strftime(fmt)
                outp.append(date)
                text = text.replace(d, '#' * len(d))
            except ValueError:
                logger.info('Specified year/month/day cannot be transformed to date')
    return outp, text


def extract_dates(text: str, today=None):
    if not today:
        today = datetime.datetime.now(tz=KST)

    if date_pattern.match(text):
        return text

    dates, text = get_regex_date(text, today)
    entities, text = extract_entities(text)

    if entities:
        values = check_combination(entities)
        for v in values:
            if convert_to_date(v, today):
                dates.append(convert_to_date(v, today))
    return dates


def extract_dates_from_to(text: str, today=None):

    def set_init_date(entities, today):
        # start with only one Relative associated entity
        relative_count = len([e for e in entities if 'Relative_' in e['entity']])
        if relative_count == 1:
            if entities[0]['entity'].startswith('Relative_Week_Future'):
                add_week = int(entities[0]['entity'][-1])
                today += datetime.timedelta(days=7 * add_week)
                entities = entities[1:]

            elif entities[0]['entity'].startswith('Relative_Month_Future'):
                add_month = int(entities[0]['entity'][-1])
                today = datetime.date(year=today.year, month=today.month+add_month, day=today.day)
                entities = entities[1:]

        # start with only one Month_P
        month_count = len([e for e in entities if e['entity'] == 'Month_P'])
        if month_count == 1:
            if entities[0]['entity'] == 'Month_P':
                try:
                    month = int(re.sub(pattern='[^\d]+', repl='', string=entities[0]['value']))
                except ValueError:
                    month = 0
                today = datetime.date(year=today.year, month=month, day=today.day)
                entities = entities[1:]

        return today, entities

    def check_is_start_end(text: str):
        text = text.replace(' ', '')
        start_end_pattern = ['#{2,3}[~-]#{2,3}']
        for p in start_end_pattern:
            if re.search(pattern=p, string=text):
                return True
        is_start = check_is_start(text)
        is_end = check_is_end(text)
        if is_start and is_end:
            return True
        else:
            return False

    def check_is_start(text: str):
        text = text.replace(' ', '')
        start_pattern = ['#부터', '#[을를]?시작']
        for p in start_pattern:
            if re.search(pattern=p, string=text):
                return True
        return False

    def check_is_end(text: str):
        text = text.replace(' ', '')
        start_pattern = ['#까지', '#[을를]?종료', '#[을를]?끝으로']
        for p in start_pattern:
            if re.search(pattern=p, string=text):
                return True
        return False

    if not today:
        today = datetime.datetime.now(tz=KST)
    outp = {
        'Start_Date': '',
        'End_Date': ''
    }
    original_text = copy.deepcopy(text)

    dates, text = get_regex_date(text, today)
    entities, text = extract_entities(text)
    today, entities = set_init_date(entities, today)

    if entities:
        values = check_combination(entities)
        for v in values:
            if convert_to_date(v, today):
                dates.append(convert_to_date(v, today))

    if len(dates) == 2:
        if check_is_start_end(text):
            start, end = sorted(dates)
            outp['Start_Date'] = start
            outp['End_Date'] = end
    elif len(dates) == 1:
        if check_is_start(text):
            outp['Start_Date'] = dates[0]
        elif check_is_end(text):
            outp['End_Date'] = dates[0]
    return outp
