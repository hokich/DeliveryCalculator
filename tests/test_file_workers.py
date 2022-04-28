import pytest

from discount_calculator import services


def create_test_data(test_data):
    with open('tests/test_input.txt', 'a') as f:
        f.writelines(test_data)


@pytest.mark.usefixtures('clean_test_file')
def test_read_from_file(example_input_data):
    create_test_data(example_input_data)
    assert services.read_text_file('tests/test_input.txt') == example_input_data


def test_splitting_lines_input_data(example_input_data):
    expected_result = [['2015-02-11', 'L', 'SimoSiuntos'], ['2015-02-12', 'M', 'JonasShipping']]
    assert services.split_lines_input_data(example_input_data) == expected_result
