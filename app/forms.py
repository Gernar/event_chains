import re


def validate_form(field):

    if field is None:
        raise BaseException('Введите корректное число или процент')
    elif re.match(r"\d+%", field):
        match = re.match(r"\d+%", field).group(0)
        if match != field:
            raise BaseException('Введите корректное число или процент')
        elif not (0 < int(match.replace('%', '')) < 100):
            raise BaseException('Процент соседей должен лежать в интервале (0, 100]')
    elif re.match(r'\d+', field):
        match = re.match(r"\d+", field).group(0)
        if match != field:
            raise BaseException('Введите корректное число или процент')
        elif not (0 < int(match)):
            raise BaseException('Число соседей должно быть больше 0')
    else:
        raise BaseException('Введите корректное число или процент')
