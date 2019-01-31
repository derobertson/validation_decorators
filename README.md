## validation_decorators

validation_decorators is a simple package that provides validation and cleansing for function arguments. It is very customizable and easy to set up.


### How to use:

1. start by downloading the package:

    ```pip install validation_decorators```

2. import your desired validation method:
    ```python
    from validation_decorators import ValidateArgType, ValidateArgAttribute, CastArg
    ```

3. create or import your error handler. This package contains a few simple error handlers, but you can easily add your own.

    ```python
    from validation_decorators.errors import log_error, raise_error, ignore_error

    type_validator = ValidateArgType(raise_error, logger=None)
    ```
4. use your decorator
   ```python
    @type_validator(id=str, value=(int, float))
    def output_item(id, title, value):
        """prints item"""
        print(f'{title}({id}): {value}')
    ```


### Usage example
```python
from validation_decorators import ValidateArgType,
from validation_decorators.errors import raise_error

type_validator = ValidateArgType(raise_error, logger=None)

@type_validator(id=str, value=int)
def output_item(id, value):
    """prints item"""
    print(f'{id}: {value}')
```

### Why?
why was this package created? Even with dynamic languages, there are times when one needs to validate function arguments, whether it be ensuring that everything is in order during development, or that you want a little extra peace of mind when collecting data from users, files, or old database tables.

Different environments and industries require different approaches to validation, and the Python community is also split on how to validate; Do you assume everything is correct, check by type, or is duck-typing your preferred method?

Even once validation preferences have been dealt with, there is another issue to tackle; If you find a validation error, how do you want to handle the error? Do you log it, throw an exception, ignore it?

Due to the large amount of variables in programming, I decided to make this package.

### Types of Decorators:
decorators are defined by creating an object from one of the decorator classes. You may also make your own class in order to help suit your needs. constructors are as follows:
```python
    decorator = ValidatorClass(error_function, logger=None)
```
* __error class__:
a function to run in the event that an argument does not match its validator. error function specifications will be described later.

* __logger__:
This is a logger object that will be used in the event that you choose to log your errors. It defaults to None, and will not be referenced unless it is called in the error function.

it should be noted that not all arguments need to be validated. only argument referenced in the decorator will be validated. all others will be passed normally.

There are two main types of decorator classes:
1. Validation

    * __ValidateArgType__: validates arguments against a single type or tuple of types. good for checking arguments based on their types. __Subclasses are considered valid__.
    ```python
    validate_args = ValidateArgType(raise_error)

    @validate_args(dt=(date, datetime))
    def date_to_yyyymmdd(dt)
    ...
    ```
    in the above example, an argument that is of the datetime or date class(as well as subclasses) will considered valid. any other type will trigger the error function.

    * __ValidateArgAttribute__: validates an argument based on its attributes. Good for duck-typing.
    ```python
    validate_args = ValidateArgType(log_error, logger=current_app.logger)

    @validate_args(dt='month')
    def date_to_yyyymmdd(dt)
    ...
    ```
    in the above example, the _dt_ argument will be considered valid if it has the attribute _month_

2. Replacement
    * __CastArg__: Useful for casting data received from a file or database. All uncastable data will be turned into a single value, making data validation and formatting a breeze.

    __note__: this class has a special argument:
     ```python
    cast_args = CastArg(ignore_error)

    class StockData():
        __slots__ = ['stock_name', 'prev_close', 'close']

        @cast_args(value_one_error='-', stock_name=str, prev_close=float, close=float)
        def __init(self, stock_name, prev_close, close):
            self.prev_close = prev_close
            if self.prev_close != '-':
                ...
    ```

    Any uncastable data will be set to _value_on_error_. _value_on_error_ defaults to None. If the argument is the same type as specified, it will simply be passed without any unnecessary casting. It should be noted that some types, especially dicts, datetimes, etc. cannot be cast with this decorator due to their nature.

    this decorator is good for controlling any unexpected values. In the above example, if prev_close was None or an empty string, it will be turned into '-'. This is helpful because all values can be tested against value_on_error. If you are displaying a the data on a website, the prev_close will be listed as a value or - without any further validation.


### Error functions
the error functions in this package are very simple in order for developers to easily change the logic to suite their use case. For example, it may be sufficient for websites to throw an exception due to global error handling, while programs may benefit from using logging.

It should be noted that _CastArg_ was created to attempt to cast values without causing errors. While you can have the decorator trigger an error, using an error function like _ignore_errors_ to suppress errors is recommended.

the error function should have the following specifications:
```python
def error_func(msg, func_name, logger):
    ...
```
#### arguments:
* __msg__ - this string will contain information about the argument that triggered the error.
* __func_name__ - this string will contain the name of the function tied to the decorator
* __msg__ - this will be a reference to the logger supplied in the constructor stated above in _documentation: Types of decorators_
