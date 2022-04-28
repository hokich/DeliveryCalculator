import datetime

import pytest

from discount_calculator import services


@pytest.mark.parametrize("date_str, date_format, expected_result", [
    ('2015-03-11', '%Y-%m-%d', True),
    ('2015-21-34', '%Y-%m-%d', False),
    ('2022-01-01', '%Y-%m-%d', True),
    ('abc', '%Y-%m-%d', False)
])
def test_string_with_date(date_str, date_format, expected_result):
    assert services.string_with_date(date_str, date_format=date_format) == expected_result


@pytest.mark.parametrize("date_str, date_format, expected_result", [
    ('2015-03-11', '%Y-%m-%d', datetime.date(year=2015, month=3, day=11)),
    ('1997-11-21', '%Y-%m-%d', datetime.date(year=1997, month=11, day=21)),
    ('1997-11-21', '%Y-%m-%d', datetime.date(year=1997, month=11, day=21)),
])
def test_converting_str_to_date(date_str, date_format, expected_result):
    assert services.convert_str_to_date(date_str, date_format=date_format) == expected_result


def test_value_error_for_converting_str_to_date():
    with pytest.raises(ValueError):
        services.convert_str_to_date('1997-14-25', date_format='%Y-%m-%d')


