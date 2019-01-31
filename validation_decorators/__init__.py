from .decorators import ReplacementDecorator, ValidationDecorator
name = 'validation_decorators'

class ValidateArgType(ValidationDecorator):
    """
    takes any number of arguments and attempts to validate them against the matching
    types in the decorator. any argument that does not match the corresponding type or types will trigger
    the error function. subclasses will be considered as matches

    example:
        @arg_decorator(k=str, v=(int,float))
        def print_number_kv(k, v):
            print(f'{k}: {v}')

        print_number(1, 2)
        in this case, this will cause an exception due to k not being a str
    """

    def __init__(self, error_function, logger=None):
        super().__init__(self._check_arg_type, error_function, logger)

    def _check_arg_type(self, arg, types):
        msg, value = '', arg
        if not isinstance(arg, types):
            msg = '%s has the type %s, not %s' %(arg, type(arg), types)
        return msg, value


class ValidateArgAttribute(ValidationDecorator):
    """
    takes any number of arguments and attempts to validate them against the matching
    attribute in the decorator. any argument that does not match the corresponding argument or arguments will trigger
    the error function

    example:
        @arg_decorator(name=strip, total=imag)
        def print_item(name, total, id):
            print(f'{name}({id}): {total}')

        print_item('a', '2', 1)
        in this case, this will cause an exception due to total not having the imag attribute
    """

    def __init__(self, error_function, logger=None):
        super().__init__(self._check_arg_attr, error_function, logger)

    def _check_arg_attr(self, arg, attribute):
        msg = ''
        if not hasattr(arg, attribute):
            msg = '%s does not have the attribute \'%s\'' %(arg, attribute)
        return msg, arg


class CastArg(ReplacementDecorator):
    """
    Takes any number of args and kwargs and attempts to cast them into the type set in the decorator.
    any uncastable items will be replaced with the value of value_on_error.
    This defaults to None

    example:
        @arg_decorator(value_on_error='-', k=str, v=int)
        def print_number_kv(k, v):
            print(f'{k}: {v}')

        print_number(2, None)
        in this case, this will cause an exception due to v not being castable into an int
    """

    def __init__(self, error_function, logger=None):
        super().__init__(self._cast_values, error_function, logger)


    def _cast_values(self, value_on_error, arg, cast_type):

        value, msg = arg, ''

        if not isinstance(arg, cast_type):
            try:
                value = cast_type(arg)
                if arg is None and cast_type is str:
                    value = value_on_error
                    msg = 'unable to cast %s into %s' % (arg, cast_type)
            except:
                msg = 'unable to cast %s into %s' % (arg, cast_type)
                value = value_on_error

        return msg, value
