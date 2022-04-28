import datetime

import pytest

from discount_calculator import models


def create_test_tariffs_objects(test_tariffs_data):
    return [models.Tariff(*tariff_data) for tariff_data in test_tariffs_data]


def test_getting_tariff_by_provider_and_package_size(tariffs_test_data_tuple):
    tariffs = create_test_tariffs_objects(tariffs_test_data_tuple)
    tariff_obj = models.Tariff.get_tariff_by_provider_and_package_size(
        tariffs, 'SimoSiuntos', 'M')
    assert isinstance(tariff_obj, models.Tariff) == True and \
           tariff_obj.provider == 'SimoSiuntos' and \
           tariff_obj.package_size == 'M' and \
           tariff_obj.price == 4.90


def test_none_returning_get_tariff_by_provider_and_package_size(tariffs_test_data_tuple):
    tariffs = create_test_tariffs_objects(tariffs_test_data_tuple)
    tariff_obj = models.Tariff.get_tariff_by_provider_and_package_size(
        tariffs, 'CUSPS', 'M')
    assert tariff_obj is None


def test_getting_tariff_with_min_price_by_package_size(tariffs_test_data_tuple):
    tariffs = create_test_tariffs_objects(tariffs_test_data_tuple)
    tariff_obj = models.Tariff.get_tariff_with_min_price_by_package_size(tariffs, 'S')
    assert isinstance(tariff_obj, models.Tariff) == True and \
           tariff_obj.provider == 'SimoSiuntos' and \
           tariff_obj.package_size == 'S' and \
           tariff_obj.price == 1.5


def test_none_returning_get_tariff_with_min_price_by_package_size(tariffs_test_data_tuple):
    tariffs = create_test_tariffs_objects(tariffs_test_data_tuple)
    tariff_obj = models.Tariff.get_tariff_with_min_price_by_package_size(tariffs, 'F')
    assert tariff_obj is None


def create_test_order_object(test_order_params):
    return models.Order(*test_order_params)


def test_getting_order_price(test_order_params):
    order = create_test_order_object(test_order_params)
    order.price = 3
    assert order.price == 3.0


@pytest.mark.parametrize("price, discount, expected_result", [
    (2, 0.5, 1.5),
    (6.9, 6.9, 0),
    (4, 2, 2),
])
def test_getting_order_discount_price(test_order_params, price, discount, expected_result):
    order = create_test_order_object(test_order_params)
    order.price = price
    order.discount = discount
    assert order.discounted_price == expected_result


@pytest.mark.parametrize("order_data, expected_result", [
    (["2015-02-01", "S", "JonasShipping"], True),
    (["2015-02-03", "M"], False),
    (["2015-02-03", 42, "SimoSiuntos"], False),
    (["2015-02-14", "M", "Siuntos"], True),
    (["02-12-2015", "M", "SimoSiuntos"], False)
])
def test_validate_order_data(order_data, expected_result):
    assert models.CreatorOrder.validate_order_data(order_data) == expected_result


def test_creating_order():
    order_data = ["2015-02-01", "S", "JonasShipping"]
    order = models.CreatorOrder.create_order(order_data)
    assert isinstance(order, models.Order) and \
    order.date == datetime.date(year=2015, month=2, day=1) and \
    order.provider == 'JonasShipping' and \
    order.package_size == 'S'


@pytest.mark.parametrize("provider, package_size, expected_result", [
    ('JonasShipping', 'S', True),
    ('Jonas', 'S', False),
    ('JonasShipping', 'XXL', False),
])
def test_verification_client_order(tariffs_test_data_tuple, provider, package_size, expected_result):
    tariffs = create_test_tariffs_objects(tariffs_test_data_tuple)
    client = models.Client()
    order = models.Order(datetime.date(year=2015, month=2, day=1), package_size, provider)
    assert models.ClientOrder(client, order).verification(tariffs) == expected_result


@pytest.mark.parametrize("client", [models.Client()])
@pytest.mark.parametrize("date, provider, package_size, expected_result", [
    (datetime.date(year=2015, month=2, day=1), 'JonasShipping', 'M', 0),
    (datetime.date(year=2015, month=2, day=1), 'JonasShipping', 'S', 0.5),
    (datetime.date(year=2015, month=2, day=2), 'SimoSiuntos', 'L', 0),
    (datetime.date(year=2015, month=2, day=3), 'SimoSiuntos', 'L', 0),
    (datetime.date(year=2015, month=2, day=4), 'SimoSiuntos', 'L', 6.9),
    (datetime.date(year=2015, month=2, day=4), 'SimoSiuntos', 'L', 0),
    (datetime.date(year=2015, month=2, day=5), 'JonasShipping', 'S', 0.5),
    (datetime.date(year=2015, month=2, day=6), 'JonasShipping', 'S', 0.5),
    (datetime.date(year=2015, month=2, day=7), 'JonasShipping', 'S', 0.5),
    (datetime.date(year=2015, month=2, day=8), 'JonasShipping', 'S', 0.5),
    (datetime.date(year=2015, month=2, day=9), 'JonasShipping', 'S', 0.5),
    (datetime.date(year=2015, month=2, day=10), 'JonasShipping', 'S', 0.1),
    (datetime.date(year=2015, month=2, day=11), 'JonasShipping', 'S', 0),
    (datetime.date(year=2015, month=3, day=1), 'JonasShipping', 'S', 0.5),
    (datetime.date(year=2015, month=3, day=2), 'SimoSiuntos', 'L', 0),
    (datetime.date(year=2015, month=3, day=3), 'SimoSiuntos', 'L', 0),
    (datetime.date(year=2015, month=3, day=4), 'SimoSiuntos', 'L', 6.9),
])
def test_discount_calculating(tariffs_test_data_tuple, client, date, provider, package_size, expected_result):
    tariffs = create_test_tariffs_objects(tariffs_test_data_tuple)
    order = models.Order(date, package_size, provider)
    assert models.Calculator.discount_calculate(tariffs, client, order) == expected_result
