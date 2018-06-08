# -*- coding: utf-8 -*-

from datetime import datetime
from konltk.nlg.datetime import DateTimeExprGenerator

import pytz

def test_datetime_expr_generator_should_make_proper_expressions():
    dt_expr_generator = DateTimeExprGenerator()
    tz = dt_expr_generator.tz

    dt_base = tz.localize(datetime(2018, 6, 6, 15))

    dt = tz.localize(datetime(2018, 6, 4, 10))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "이번주 월요일(4일) 오전 10시"

    dt = tz.localize(datetime(2018, 6, 5, 18))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "어제(5일) 오후 6시"

    dt = tz.localize(datetime(2018, 6, 6, 8))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "오늘 오전 8시"

    dt = tz.localize(datetime(2018, 6, 7, 22, 10))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "내일 오후 10시 10분"

    dt = tz.localize(datetime(2018, 6, 8, 23))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "모레(8일) 오후 11시"

    dt = tz.localize(datetime(2018, 6, 9, 12))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "토요일(9일) 오후 12시"

    dt = tz.localize(datetime(2018, 6, 11, 12))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "다음주 월요일(11일) 오후 12시"

    dt = tz.localize(datetime(2018, 6, 1))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "지난주 금요일(1일) 오전 12시"

    dt = tz.localize(datetime(2018, 5, 30, 8, 21))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "2018년 5월 30일 수요일, 오전 8시 21분"

    dt = tz.localize(datetime(2018, 4, 1, 11))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "2018년 4월 1일 일요일, 오전 11시"

    dt = tz.localize(datetime(2018, 7, 21, 15, 10, 30))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "7월 21일 토요일, 오후 3시 10분 30초"

    dt = tz.localize(datetime(2018, 8, 4, 16, 0, 0))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "8월 4일 토요일, 오후 4시"

    dt = tz.localize(datetime(2019, 1, 21, 15, 0, 10))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "2019년 1월 21일 월요일, 오후 3시 0분 10초"

    dt = tz.localize(datetime(2019, 2, 4, 16))
    expr = dt_expr_generator.generate(dt, dt_base=dt_base)
    assert expr == "2019년 2월 4일 월요일, 오후 4시"

def test_datetime_expr_generator_should_make_proper_range_expressions():
    dt_expr_generator = DateTimeExprGenerator()
    tz = dt_expr_generator.tz

    dt_base = tz.localize(datetime(2018, 6, 6, 15))

    dt_start = tz.localize(datetime(2018, 6, 4, 10))
    dt_end = tz.localize(datetime(2018, 6, 4, 14))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "이번주 월요일(4일) 오전 10시부터 오후 2시"

    dt_start = tz.localize(datetime(2018, 6, 5, 18))
    dt_end = tz.localize(datetime(2018, 6, 5, 21))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "어제(5일) 오후 6시부터 9시"

    dt_start = tz.localize(datetime(2018, 6, 6, 8))
    dt_end = tz.localize(datetime(2018, 6, 6, 11))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "오늘 오전 8시부터 11시"

    dt_start = tz.localize(datetime(2018, 6, 7, 22, 10))
    dt_end = tz.localize(datetime(2018, 6, 8, 22, 10))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "내일 오후 10시 10분부터 모레(8일) 오후 10시 10분"

    dt_start = tz.localize(datetime(2018, 6, 8, 23))
    dt_end = tz.localize(datetime(2018, 6, 10, 23))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "모레(8일) 오후 11시부터 10일 일요일 오후 11시"

    dt_start = tz.localize(datetime(2018, 6, 9, 12))
    dt_end = tz.localize(datetime(2018, 6, 16, 12))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "토요일(9일) 오후 12시부터 다음주 토요일(16일) 오후 12시"

    dt_start = tz.localize(datetime(2018, 6, 11, 12))
    dt_end = tz.localize(datetime(2018, 6, 4, 16))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "다음주 월요일(11일) 오후 12시부터 이번주 월요일(4일) 오후 4시"

    dt_start = tz.localize(datetime(2018, 6, 1))
    dt_end = tz.localize(datetime(2018, 6, 4))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "지난주 금요일(1일) 오전 12시부터 이번주 월요일(4일) 오전 12시"

    dt_start = tz.localize(datetime(2018, 5, 30, 8, 21))
    dt_end = tz.localize(datetime(2018, 5, 31, 8, 20))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "2018년 5월 30일 수요일, 오전 8시 21분부터 31일 목요일 오전 8시 20분"

    dt_start = tz.localize(datetime(2018, 4, 1, 11))
    dt_end = tz.localize(datetime(2019, 3, 31, 11))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "2018년 4월 1일 일요일, 오전 11시부터 2019년 3월 31일 일요일, 오전 11시"

    dt_start = tz.localize(datetime(2018, 7, 21, 15, 10, 30))
    dt_end = tz.localize(datetime(2018, 7, 23, 15, 10, 30))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "7월 21일 토요일, 오후 3시 10분 30초부터 23일 월요일 오후 3시 10분 30초"

    dt_start = tz.localize(datetime(2018, 8, 4, 16, 0, 0))
    dt_end = tz.localize(datetime(2019, 8, 4, 16, 0, 0))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "8월 4일 토요일, 오후 4시부터 2019년 8월 4일 일요일, 오후 4시"

    dt_start = tz.localize(datetime(2019, 1, 21, 15, 0, 10))
    dt_end = tz.localize(datetime(2018, 1, 21, 15, 0, 10))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "2019년 1월 21일 월요일, 오후 3시 0분 10초부터 2018년 1월 21일 일요일, 오후 3시 0분 10초"

    dt_start = tz.localize(datetime(2019, 2, 4, 16))
    dt_end = tz.localize(datetime(2018, 6, 6, 10))
    expr = dt_expr_generator.generate(dt_start, dt_end, dt_base=dt_base)
    assert expr == "2019년 2월 4일 월요일, 오후 4시부터 2018년 6월 6일 수요일, 오전 10시"

