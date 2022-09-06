from datetime import datetime, date
from functools import wraps
import arrow


def format_if_date(item, arrow_format: str = "YYYY-MM-DD"):
    """
    If `item` is of type `datetime.datetime` or `datetime.date` converts it to `str`
    using `fmt` expression, otherwise returns `item` as is.

    Usage:
    >>> format_if_date(datetime(2022, 1, 1, 9, 30))
    2022-01-01
    >>> format_if_date(datetime(2022, 1, 1, 9, 30), "YYYY.MM.DD")
    2022.01.01
    """
    if isinstance(item, (datetime, date)):
        arrow_date = arrow.get(item)
    elif isinstance(item, arrow.Arrow):
        arrow_date = item
    else:
        return item

    return arrow_date.format(arrow_format)


def format_date_args(arrow_format: str):
    """
    Decorator that converts `datetime.datetime` or `datetime.date` arguments into `str`
    using the `date_format` specification.

    Usage:
    >>> @format_date_args("YYYY-MM-DD")
    ... def f(arg):
    ...     print(arg)
    >>> f(datetime(2022, 1, 1, 9, 30))
    2022-01-01
    """
    fmt = arrow_format
    def decorate(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            updated_args = [format_if_date(arg, fmt) for arg in args]
            updated_kwargs = {k: format_if_date(v, fmt) for k, v in kwargs.items()}

            return f(*updated_args, **updated_kwargs)
        return wrapper
    return decorate
