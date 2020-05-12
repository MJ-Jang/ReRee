#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division

import datetime
import re
import copy
import logging

from reree.utils import normalize_Count_time

logger = logging.getLogger()

fmt = '%Y.%m.%d'
date_pattern = re.compile(pattern='20\\d{2}\\.[0-1]\\d\\.[0-3]\\d')
KST = datetime.timezone(datetime.timedelta(hours=9))
days = ['월', '화', '수', '목', '금', '토', '일']

# sequence is important

specialMappingDict = {
    "Week_day": {
        '불금': '금요일',
        '주말': '토요일',
        '주일': '일요일'
    }
}


# 1. extract time related entities from entity extracted
def extract_date_entities(entities: list):
    timeEntities = ['Year', 'Month', 'Week', 'Date', 'Stay_Period']
    outp = []
    for e in entities:
        for te in timeEntities:
            if te in e['entity']:
                outp.append(e)
    if outp:
        outp = sorted(outp, key=lambda x: x['start'])
    return outp


def check_combination(entities: list):
    outp = []
    if entities[0]['entity'] in ['Date', 'Week_day', 'Relative_Date_Present',
                                 'Relative_Date_Future_1', 'Relative_Date_Future_2']:
        tmp = {
            'comb': [entities[0]['entity']],
            str(entities[0]['entity']): entities[0]['value']
        }
        outp.append(tmp)

    for i in range(1, len(entities)):
        # Date rule
        if entities[i]['entity'] == 'Date':
            if entities[i - 1]['entity'] in ['Month', 'Relative_Month_Present',
                                             'Relative_Month_Future_1', 'Relative_Month_Future_2']:
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
            if entities[i - 1]['entity'] in ['Relative_Week_Present', 'Relative_Week_Future_1', 'Relative_Week_Future_2']:
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


def return_period_adddates(value: str) -> int:
    add_dates = 0

    addition_dict = {'일': 1, '주': 7, '달': 30, '년': 365}
    period_pattern = re.compile('\d{1,2}[일주달년]')

    value = normalize_Count_time(value)
    period_ = period_pattern.findall(value)
    if period_:
        unit = period_[0][-1]
        add_dates += int(re.compile('[^\d]+').sub('', period_[0])) * addition_dict[unit]
    return add_dates


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

    if cand['comb'] == ['Date']:
        day = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Date']))
        if day:
            date = set_date(year=today.year, month=today.month, day=day)
        else:
            logger.info('Cannot know exact number of specified date')

    if cand['comb'] == ['Month_P', 'Date']:
        month = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Month']))
        day = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Date']))
        if month and day:
            date = set_date(year=today.year, month=month, day=day)
        else:
            logger.info('Cannot know exact number of specified date')

    if cand['comb'] == ['Relative_Month_Present', 'Date']:
        day = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Date']))
        if day:
            date = set_date(year=today.year, month=today.month, day=day)
        else:
            logger.info('Cannot know exact number of specified date')

    if cand['comb'] == ['Relative_Month_Future_1', 'Date']:
        day = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Date']))
        if day:
            date = set_date(year=today.year, month=today.month + 1, day=day)
        else:
            logger.info('Cannot know exact number of specified date')

    if cand['comb'] == ['Relative_Month_Future_2', 'Date']:
        day = int(re.sub(pattern='[^0-9]+', repl='', string=cand['Date']))
        if day:
            date = set_date(year=today.year, month=today.month + 2, day=day)
        else:
            logger.info('Cannot know exact number of specified date')

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

    if cand['comb'] == ['Relative_Week_Future_2', 'Week_day']:
        day = transform_weekday(cand['Week_day'])
        today_day = days[datetime.datetime.today().weekday()]
        diff = days.index(day) - days.index(today_day)
        date = today + datetime.timedelta(days=14 + diff)

    if date:
        return date.strftime(fmt)
    else:
        return ''


def extract_dates_from_to(text: str, entities: list, today=None):

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
        month_count = len([e for e in entities if e['entity'] == 'Month'])
        if month_count == 1:
            if entities[0]['entity'] == 'Month':
                try:
                    month = int(re.sub(pattern='[^\d]+', repl='', string=entities[0]['value']))
                except ValueError:
                    month = 0
                today = datetime.date(year=today.year, month=month, day=today.day)
                entities = entities[1:]

        return today, entities

    def basic_preprocess(entities, text, today):
        dates = []
        for e in entities:
            if e['entity'] == 'Date_Format_YMD':
                year, month, day = [int(s.strip()) for s in re.split(pattern='[\\s\\.\\-/]+', string=e['value'])]
                try:
                    date = datetime.date(year=year, month=month, day=day).strftime(fmt)
                    dates.append(date)
                except ValueError:
                    logger.info('Specified date is not proper value')
            elif e['entity'] == 'Date_Format_MD':
                month, day = [int(re.sub(pattern='[^\\d]+', repl='', string=s).strip())
                              for s in re.split(pattern='[\\s\\.\\-/]+', string=e['value'])]
                try:
                    date = datetime.date(year=today.year, month=month, day=day).strftime(fmt)
                    dates.append(date)
                except ValueError:
                    logger.info('Specified date is not proper value')

            text = text.replace(e['value'], '#' * len(e['value']))
        return dates, text

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

    entities = extract_date_entities(entities)
    dates, text = basic_preprocess(entities, text, today)
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
            # Stay period logic
            if 'Stay_Period' in [e['entity'] for e in entities]:
                period_value = list(filter(lambda x: x['entity'] == 'Stay_Period', entities))
                value = period_value[0]['value']

                year, month, day = [int(s.strip()) for s in re.split(pattern='[\\s\\.\\-/]+', string=dates[0])]
                add_dates = return_period_adddates(value)
                date = datetime.date(year=year, month=month, day=day) + datetime.timedelta(days=add_dates)
                date = date.strftime(fmt)
                outp['End_Date'] = date
        elif check_is_end(text):
            outp['End_Date'] = dates[0]
    return outp
