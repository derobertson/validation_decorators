from functools import wraps

class BaseDecorator():
    _error_function = None
    _validation_function = None
    _logger = None

    def __init__(self, validation_function, error_function, logger=None):

        self._validation_function = validation_function
        self._error_function = error_function
        self._logger = logger

    __init__.__doc__ = __doc__

class ReplacementDecorator(BaseDecorator):
    def __call__(self, value_on_error=None, **arg_to_check):
        return self._arg_replace(value_on_error, **arg_to_check)

    def _arg_replace(self, value_on_error=None, **arg_to_check):
        """
        takes any number of args and kwargs coupled with a validator and passes
        them to a validation function. This function also takes a value on error argument.
        this will be used to replace the given value when the validation function fails

        example for CastArg:
            value_on_error='-', a=int, bool, str

            any arguments that cannot be cast into corresponding type will be replace with '-'
        """
        def _on_decorator_call(func):
            all_args = list(func.__code__.co_varnames)

            @wraps(func)
            def _on_call(*args, **kwargs):
                positional_args = all_args[:len(args)]

                new_args = list(args)
                for (arg_name, replace) in arg_to_check.items():
                    if arg_name in kwargs:
                        msg, val = self._validation_function(value_on_error, kwargs[arg_name], replace)
                        kwargs[arg_name] = val
                    elif arg_name in positional_args:
                        msg, val = self._validation_function(value_on_error, args[positional_args.index(arg_name)], replace)
                        new_args[positional_args.index(arg_name)] = val
                    if msg != '':
                        self._error_function(msg, func.__name__, self._logger)

                args = tuple(new_args)

                return func(*args, **kwargs)
            return _on_call
        return _on_decorator_call


class ValidationDecorator(BaseDecorator):
    def __call__(self, **arg_to_check):
        return self._arg_validate(**arg_to_check)

    def _arg_validate(self, validate_func=None, error_func=None, **arg_to_check):
        """
        takes any number of args and kwargs coupled with a validator and passes
        them to the passed validation function.

        example for ValidateArgType:
            a=int, bool, str

            any value that does not have the same type as stated in the decorator will
            result in the error function being called
        """

        def on_decorator_call(func):
            all_args = list(func.__code__.co_varnames)

            @wraps(func)
            def on_call(*args, **kwargs):
                positional_args = all_args[:len(args)]

                msg = ''
                for (arg_name, validators) in arg_to_check.items():
                    if arg_name in kwargs:
                        msg, _ = self._validation_function(kwargs[arg_name], validators)
                    elif arg_name in positional_args:
                        msg, _ = self._validation_function(args[positional_args.index(arg_name)], validators)

                    if msg != '':
                        self._error_function(msg, func.__name__, self._logger)

                return func(*args, **kwargs)
            return on_call
        return on_decorator_call
