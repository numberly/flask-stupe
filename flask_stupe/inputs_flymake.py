__all__ = ["boolean"]


# vtr: This function belongs to https://github.com/flask-restful/flask-restful
# It is licensed under the BSD 3-clause "New" or "Revised" License
# https://github.com/flask-restful/flask-restful/blob/master/LICENSE
def boolean(value):
    """Parse the string ``"true"`` or ``"false"`` as a boolean (case
    insensitive). Also accepts ``"1"`` and ``"0"`` as ``True``/``False``
    (respectively). If the input is from the request JSON body, the type is
    already a native python boolean, and will be passed through without
    further parsing.
    """
    if isinstance(value, bool):
        return value

    if not value:
        raise ValueError("boolean type must be non-null")
    value = value.lower()
    if value in ('true', '1',):
        return True
    if value in ('false', '0',):
        return False
    raise ValueError("Invalid literal for boolean(): {0}".format(value))
