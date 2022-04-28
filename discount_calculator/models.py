import datetime

import configs
from . import services


class Client:
    """
    The class describing the client
    """
    def __init__(self):
        """
        :discount_amount: float
        :last_order_date: datetime.date
        """
        self.discount_amount = 0
        self.last_order_month = 0
        self.orders_count_l_size_from_simo_siuntos = 0


class Tariff:
    """
    The class describing the tariff
    Init params:
    :provider: str - provider name
    :package_size: str
    :price: float
    """
    def __init__(self, provider: str, package_size: str, price):
        self.provider = provider
        self.package_size = package_size
        self.price = price

    @staticmethod
    def add_tariffs_from_tuple(tariffs_data: tuple) -> list:
        """
        Creating instances of the Tariff class. Accepts a tuple with fare data.
        :param tariffs_data:
        Example tariffs_data
        (
            ('SimoSiuntos', 'S', 1.50),
            ('SimoSiuntos', 'M', 4.90),
            ('SimoSiuntos', 'L', 6.90),
            ('JonasShipping', 'S', 2),
            ('JonasShipping', 'M', 3),
            ('JonasShipping', 'L', 4),
        )
        :return:
        """
        return [Tariff(*tariff_data) for tariff_data in tariffs_data]

    @staticmethod
    def get_tariff_by_provider_and_package_size(tariffs: list, provider: str, package_size: str):
        """
        Get a instance of the Tariff by the name and size of the package.
        :param tariffs: list - tariffs objects list
        :param provider:
        :param package_size:
        :return: Tariff or None
        """
        tariffs = list(filter(
            lambda tariff: tariff.provider == provider and tariff.package_size == package_size, tariffs
        ))
        return tariffs[0] if tariffs else None

    @staticmethod
    def get_tariff_with_min_price_by_package_size(tariffs: list, package_size: str):
        """
        Get a instance of the Tariff by the name and size of the package
        :param tariffs: Tariffs list
        :param package_size:
        :return: :return: Tariff or None
        """
        tariffs = list(filter(lambda tariff: tariff.package_size == package_size, tariffs))
        return min(tariffs, key=lambda tariff: tariff.price) if tariffs else None


class Order:
    """
    The class describing the order. Accepts valid order data.
    Init params:
    :date: datetime.date - order date
    :package_size: str
    :provider: str
    """
    def __init__(self, date: datetime.date, package_size: str, provider: str):
        self.date = date
        self.package_size = package_size
        self.provider = provider

        self._price = 0
        self._discount = 0

    def __repr__(self):
        return f"{self.date_str} {self.package_size} {self.provider}"

    def __str__(self):
        return f'{self.date_str} {self.package_size} {self.provider} ' \
               f'{self.discounted_price} {self.discount if self.discount else "-"}'

    @property
    def date_str(self) -> str:
        """
        Getting the date as a string
        :return:
        """
        return self.date.strftime('%Y-%m-%d')

    @property
    def price(self) -> float:
        """
        Price property rounded to 2 decimal places
        :return:
        """
        return round(self._price, 2)

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def discount(self) -> float:
        """
        Discount property rounded to 2 decimal places
        :return:
        """
        return round(self._discount, 2)

    @discount.setter
    def discount(self, value):
        self._discount = value

    @property
    def discounted_price(self) -> float:
        """
        Calculating the price with a discount
        :return:
        """
        return self.price - self.discount if self.discount else self.price


class CreatorOrder:
    """
    Auxiliary class for validating order data and order creation
    """
    @staticmethod
    def create_order(order_data: list) -> Order:
        """
        Creating an order. Accepts a list of valid order data.
        Example order_data:
        ["2015-02-01", "S", "JonasShipping"]
        :param order_data:
        :return:
        """
        date = services.convert_str_to_date(order_data[0])
        order = Order(date, order_data[1], order_data[2])
        return order

    @staticmethod
    def validate_order_data(order_data: list) -> bool:
        """
        Order data validation.
        Example order_data:
        ["2015-02-01", "S", "JonasShipping"]
        :return:
        """
        if len(order_data) != 3:
            return False

        if not services.string_with_date(order_data[0]):
            return False

        if type(order_data[1]) != str:
            return False

        if type(order_data[1]) != str:
            return False

        return True


class ClientOrder:
    """
    A class for order connection with the client.
    Init params:
    :client: Client - client object
    :order: Order - order object
    """
    def __init__(self, client: Client, order: Order):
        self.client = client
        self.order = order

    def verification(self, tariffs: list) -> bool:
        """
        Verification of the order (Verification of the ability to execute the order).
        In this case the availability of the required tariff is checked.
        :param tariffs: list(Tariff) - tariffs objects list
        :return: bool
        """
        if not Tariff.get_tariff_by_provider_and_package_size(tariffs, self.order.provider, self.order.package_size):
            return False
        return True


class Calculator:
    """
    Calculator class for calculating delivery costs.
    """
    @staticmethod
    def discount_calculate(tariffs: [Tariff], client: Client, order: Order) -> float:
        """
        Method for calculating the shipping discount by rules.
        :param tariffs: - tariffs objects list
        :param client: - Client object
        :param order: - Order object
        :return: float - discount
        """
        discount = 0

        # If the month number of the current order differs from the month number
        # set by the customer, then reset the parameters
        # orders_count_l_size_from_simo_siuntos and discount_amount.
        # And update last_order_month for client
        if client.last_order_month != order.date.month:
            client.discount_amount = 0
            client.orders_count_l_size_from_simo_siuntos = 0
            client.last_order_month = order.date.month

        # Getting current tariff for order
        current_tariff = Tariff.get_tariff_by_provider_and_package_size(tariffs, order.provider, order.package_size)

        # Rule: All S shipments should always match the lowest S package price among the providers.
        if order.package_size == 'S':
            s_tariff_with_min_price = Tariff.get_tariff_with_min_price_by_package_size(tariffs, order.package_size)
            if s_tariff_with_min_price:
                discount = current_tariff.price - s_tariff_with_min_price.price

        # Rule: The third L shipment via SimoSiuntos should be free, but only once a calendar month.
        if order.provider == 'SimoSiuntos' and order.package_size == 'L':
            client.orders_count_l_size_from_simo_siuntos += 1
            if client.orders_count_l_size_from_simo_siuntos == 3:
                discount = current_tariff.price

        # Rule: Accumulated discounts cannot exceed 10 € in a calendar month.
        # If there are not enough funds to fully cover a discount
        # this calendar month, it should be covered partially.
        if client.discount_amount <= configs.MAX_DISCOUNT_PER_MONTH:
            if client.discount_amount + discount > configs.MAX_DISCOUNT_PER_MONTH:
                discount = configs.MAX_DISCOUNT_PER_MONTH - client.discount_amount
            client.discount_amount += discount

        return round(discount, 2)
