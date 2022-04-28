import configs
from discount_calculator import models, services


if __name__ == '__main__':
    output_orders_list = []

    # Getting orders data from file "input.txt"
    text_data_list = services.read_text_file('input.txt')
    orders_clean_data_list = services.split_lines_input_data(text_data_list)

    # Creating client object
    client = models.Client()

    # Creating tariffs objects from tuple from config.py
    tariffs = models.Tariff.add_tariffs_from_tuple(configs.TARIFFS_DATA)

    for order_clean_data in orders_clean_data_list:

        # Validation of order input data. If validation fails - add invalid data to the
        # output data list by adding the word "Ignored". And continue.
        if not models.CreatorOrder.validate_order_data(order_clean_data):
            output_orders_list.append(f"{' '.join(order_clean_data)} Ignored\n")
            continue

        # Creating an order and linking it to the client
        order_obj = models.CreatorOrder.create_order(order_clean_data)
        client_order = models.ClientOrder(client, order_obj)

        # Verification of the order. If verification fails - add invalid data to the
        # output data list by adding the word "Not confirmed". And continue.
        if not client_order.verification(tariffs):
            output_orders_list.append(f"{' '.join(order_clean_data)} Not confirmed\n")
            continue

        # Getting tariff for this order and setting order price without discount
        tariff = models.Tariff.get_tariff_by_provider_and_package_size(
            tariffs, order_obj.provider, order_obj.package_size)
        order_obj.price = tariff.price

        # Calculating and setting discount price for this order
        order_obj.discount = models.Calculator.discount_calculate(tariffs, client, order_obj)

        # Add order data to the output list
        output_orders_list.append(f'{str(order_obj)}\n')

    services.write_text_file('output.txt', output_orders_list)
