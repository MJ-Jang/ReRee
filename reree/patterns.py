#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, division


DATE_PATTERN = {
    '1일': ['일일', '하루'],
    '2일': ['이일', '이틀'],
    '3일': ['삼일', '사흘'],
    '4일': ['사일', '나흘'],
    '5일': ['오일', '닷새'],
    '6일': ['육일', '엿새'],
    '7일': ['칠일', '이레'],
    '8일': ['팔일', '여드레'],
    '9일': ['구일', '아흐레'],
    '10일': ['십일',	'열흘'],
    '15일': ['십오일', '보름'],
}

WEEK_PATTERN = {
    '1주	': ['일주일?', '한\\s?주'],
    '2주	': ['이주일?', '두\\s?주'],
    '3주	': ['삼주일?', '세\\s?주'],
    '4주	': ['사주일?', '네\\s?주'],
    '5주	': ['오주일?', '다섯\\s?주'],
    '6주	': ['육주일?', '여섯\\s?주'],
    '7주	': ['칠주일?', '일곱\\s?주'],
    '8주	': ['팔주일?', '여덟\\s?주'],
    '9주	': ['구주일?', '아홉\\s?주'],
}

MONTH_PATTERN = {
    '1개월':	['1달', '한\\s?달', '일개월'],
    '2개월':	['2달', '두\\s?달', '이개월'],
    '3개월':	['3달', '세\\s?달', '삼개월', '석달'],
    '4개월':	['4달', '네\\s?달', '사개월', '넉달'],
    '5개월':	['5달', '다섯\\s?달', '오개월'],
    '6개월':	['6달', '여섯\\s?달', '육개월'],
    '7개월':	['7달', '일곱\\s?달', '칠개월'],
    '8개월': ['8달', '여덟\\s?달', '팔개월'],
    '9개월': ['9달', '아홉\\s?달', '구개월'],
    '10개월': ['10달', '열\\s?달', '십개월'],
    '11개월': ['11달', '열한\\s?달', '십일개월'],
    '12개월': ['12달', '열두\\s?달', '십이개월'],
}


MONTH_PATTERN_STACTIC = {
    '1월':	['일월'],
    '2월':	['이월'],
    '3월':	['삼월'],
    '4월':	['사월'],
    '5월':	['오월'],
    '6월':	['육월', '유월'],
    '7월':	['칠월'],
    '8월':  ['팔월'],
    '9월':  ['구월'],
    '10월': ['십월', '시월'],
    '11월': ['십일월'],
    '12월': ['십이월'],
}

YEAR_PATTERN = {
    '1년': ['한\\s?해', '일년'],
    '2년': ['두\\s?해', '이년'],
    '3년': ['세\\s?해', '삼년'],
    '4년': ['네\\s?해', '사년'],
}
