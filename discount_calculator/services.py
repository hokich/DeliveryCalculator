import datetime


def read_text_file(file_path: str) -> list:
    """
    Read text data from file. Return test lines list
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as f:
        return f.readlines()


def split_lines_input_data(lines_list):
    """
    Split lines by spaces from lines list
    :param lines_list:
    :return:
    """
    return [line.split() for line in lines_list]


def write_text_file(file_path: str, lines_list: list):
    """
    Write text data in file
    :param file_path:
    :param lines_list:
    :return:
    """
    with open(file_path, 'w') as f:
        f.writelines(lines_list)


def string_with_date(date_str: str, date_format='%Y-%m-%d') -> bool:
    """
    Checking the string for a date
    :param date_str:
    :param date_format:
    :return:
    """
    try:
        datetime.datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def convert_str_to_date(date_str: str, date_format='%Y-%m-%d') -> datetime.date:
    """
    Convert string to date
    :param date_str:
    :param date_format:
    :return:
    """
    return datetime.datetime.strptime(date_str, date_format).date()

