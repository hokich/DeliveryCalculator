import datetime

import pytest


@pytest.fixture
def clean_test_file():
    with open('tests/test_input.txt', 'w'):
        pass


@pytest.fixture
def example_input_data():
    return ['2015-02-11 L SimoSiuntos\n', '2015-02-12 M JonasShipping\n']


@pytest.fixture
def tariffs_test_data_tuple():
    return (
        ('SimoSiuntos', 'S', 1.50),
        ('SimoSiuntos', 'M', 4.90),
        ('SimoSiuntos', 'L', 6.90),
        ('JonasShipping', 'S', 2),
        ('JonasShipping', 'M', 3),
        ('JonasShipping', 'L', 4),
    )


@pytest.fixture
def test_order_params():
    return datetime.date(year=2015, month=3, day=14), 'M', 'JonasShipping'
