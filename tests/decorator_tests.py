import unittest
from validation_decorators import errors, ValidateArgType, ValidateArgAttribute, CastArg
from datetime import date, datetime
from decimal import Decimal

class ValidateArgTypeTestDecorator(unittest.TestCase):
    """Tests ValidateArgType with a function that raises a type error when an argument does not match its corresponding type"""

    def setUp(self):
        def error_func(msg, func_name, logger):
            raise TypeError("error in %s: %s" % (func_name, msg))

        self.check_arg_types = ValidateArgType(error_func)


    def test_single_arg_single_type(self):
        """Test single argument against a single type"""

        @self.check_arg_types(a=str)
        def return_values(a):
            return (a,)

        self.assertEqual(return_values('a'), ('a',))

        with self.assertRaises(TypeError):
            return_values(1)


    def test_single_arg_multiple_types(self):
        """Test single argument against multiple types"""

        @self.check_arg_types(a=(int, Decimal))
        def return_values(a):
            return (a,)

        self.assertEqual(return_values(1), (1,))

        self.assertEqual(return_values(Decimal('1.500')), (Decimal('1.500'),))

        with self.assertRaises(TypeError):
            return_values(1.5)


    def test_kw_arg(self):
        """Test to ensure that decorator keyword and function keywords match"""

        @self.check_arg_types(a=list)
        def return_values(a, b):
            return (a, b)

        self.assertEqual(return_values(a=[1, 2], b=0), ([1, 2], 0))

        self.assertEqual(return_values(b=0, a=[1, 2]), ([1, 2], 0))

        with self.assertRaises(TypeError):
            return_values(a=1, b=0)

        with self.assertRaises(TypeError):
            return_values(b=0, a=1)


    def test_multiple_args(self):
        """Testing multiple arguments and types"""

        @self.check_arg_types(id=int, create_date=datetime, title=str, val=(int, float))
        def output_item(id, create_date, title, val):
            return (id, create_date, title, val)

        dt = datetime.now()

        self.assertEqual(output_item(id=1, create_date=dt, title='test', val=1), (1, dt, 'test', 1))

        self.assertEqual(output_item(id=1, create_date=dt, title='test', val=1.5), (1, dt, 'test', 1.5))

        with self.assertRaises(TypeError):
            output_item(id='1', create_date=dt, title='test', val=1)

        with self.assertRaises(TypeError):
            output_item(id=1, create_date=None, title='test', val=1)

        with self.assertRaises(TypeError):
            output_item(id=1, create_date=dt, title={'a': '1'}, val=1)

        with self.assertRaises(TypeError):
            output_item(id=1, create_date=dt, title='test', val=Decimal('-1.3'))

        with self.assertRaises(TypeError):
            output_item(id=None, create_date=None, title=None, val=None)


    def test_multiple_args_ignored_args(self):
        """Testing multiple arguments and types when some arguments are not specified in decorator"""

        @self.check_arg_types(id=int, create_date=datetime, val=(int, float))
        def output_item(id, create_date, title, val):
            return (id, create_date, title, val)

        dt = datetime.now()

        self.assertEqual(output_item(id=1, create_date=dt, title='test', val=1), (1, dt, 'test', 1))

        self.assertEqual(output_item(id=1, create_date=dt, title=1, val=1), (1, dt, 1, 1))

        self.assertEqual(output_item(id=1, create_date=dt, title=None, val=1.5), (1, dt, None, 1.5))

        with self.assertRaises(TypeError):
            output_item(id='1', create_date=dt, title='test', val=1)

        with self.assertRaises(TypeError):
            output_item(id=1, create_date=None, title='test', val=1)

        with self.assertRaises(TypeError):
            output_item(id=1, create_date=dt, title='test', val=Decimal('-1.3'))

        with self.assertRaises(TypeError):
            output_item(id=None, create_date=None, title=None, val=None)


    def test_subclass(self):
        """Test to ensure that subclasses match"""

        class SubList(list):
            pass
        sub = SubList([1, 2])

        @self.check_arg_types(a=list)
        def return_values(a, b):
            return (a, b)

        self.assertEqual(return_values(a=sub, b=0), (sub, 0))



class CastArgDecoratorTest(unittest.TestCase):
    """Tests CastArg with an custom error function that does not trigger any exceptions or error messages. any uncastable arguments will be set to None"""

    def setUp(self):
        def error_func(msg, func_name, logger):
            pass

        self.check_arg_types = CastArg(error_func)


    def test_single_arg(self):
        """Test single argument against a single type"""

        @self.check_arg_types(value_on_error=None, a=str)
        def return_values(a):
            return (a,)

        self.assertEqual(return_values(1), ('1',))

        self.assertEqual(return_values('a'), ('a',))

        self.assertEqual(return_values({'a': 1}), ("{'a': 1}",))

        self.assertEqual(return_values(date.today()), (str(date.today()),))


    def test_kw_arg(self):
        """Test to ensure that decorator keyword and function keywords match"""

        @self.check_arg_types(value_on_error=None, a=int)
        def return_values(a, b):
            return (a, b)

        self.assertEqual(return_values(a=[1, 2], b=0), (None, 0))

        self.assertEqual(return_values(b=0, a=Decimal('1.400')), (1, 0))


    def test_multiple_args(self):
        """Testing multiple arguments and types"""

        @self.check_arg_types(value_on_error=None, id=int, create_date=datetime, title=str)
        def output_item(id, create_date, title):
            return (id, create_date, title)

        dt = datetime.now()

        self.assertEqual(output_item(id=1, create_date=dt, title='test'), (1, dt, 'test'))
        self.assertEqual(output_item(id='1', create_date=dt, title='test'), (1, dt, 'test'))
        self.assertEqual(output_item(id=1.4, create_date=dt, title='test'), (1, dt, 'test'))
        self.assertEqual(output_item(id=[1, 2], create_date=dt, title='test'), (None, dt, 'test'))

        self.assertEqual(output_item(id=1, create_date=dt, title='test'), (1, dt, 'test'))
        self.assertEqual(output_item(id=1, create_date='2019/01/25', title='test'), (1, None, 'test'))
        self.assertEqual(output_item(id=1, create_date=date.today(), title='test'), (1, None, 'test'))

        self.assertEqual(output_item(id=1, create_date=dt, title=1), (1, dt, '1'))
        self.assertEqual(output_item(id=1, create_date=dt, title=dt), (1, dt, str(dt)))
        self.assertEqual(output_item(id=1, create_date=dt, title=None), (1, dt, None))

        self.assertEqual(output_item(id=1, create_date=dt, title=[1, 2]), (1, dt, str([1, 2])))


    def test_multiple_args_ignored_args(self):
        """Testing multiple arguments and types when some arguments are not specified in decorator"""

        @self.check_arg_types(id=int, create_date=datetime, val=int)
        def output_item(id, create_date, title, val):
            return (id, create_date, title, val)

        dt = datetime.now()

        self.assertEqual(output_item(id='1', create_date=dt, title='test', val=1), (1, dt, 'test', 1))
        self.assertEqual(output_item(id=1, create_date='a', title=1, val=1), (1, None, 1, 1))
        self.assertEqual(output_item(id=1, create_date=dt, title=None, val=1.5), (1, dt, None, 1))



class ValidatetArgAttributeDecoratorTest(unittest.TestCase):
    """Tests ValidateArgAttribute with a function that raises a type error when an argument does not have its corresponding attribute"""

    def setUp(self):
        def error_func(msg, func_name, logger):
            raise AttributeError("error in %s: %s" % (func_name, msg))

        self.check_arg_attrs = ValidateArgAttribute(error_func)


    def test_single_arg_single_type(self):
        """Test single argument against a single attribute"""

        @self.check_arg_attrs(a='upper')
        def return_values(a):
            return (a,)

        self.assertEqual(return_values('a'), ('a',))

        self.assertEqual(return_values('a'), ('a',))

        with self.assertRaises(AttributeError):
            return_values(1)


    def test_kw_arg(self):
        """Test to ensure that decorator keyword and function keywords match"""

        @self.check_arg_attrs(a='append')
        def return_values(a, b):
            return (a, b)

        self.assertEqual(return_values(a=[1, 2], b=0), ([1, 2], 0))

        self.assertEqual(return_values(b=0, a=[1, 2]), ([1, 2], 0))

        with self.assertRaises(AttributeError):
            return_values(a=1, b=0)

        with self.assertRaises(AttributeError):
            return_values(b=0, a=1)


    def test_multiple_args(self):
        """Testing multiple arguments"""

        @self.check_arg_attrs(id='real', create_date='month', title='strip', val='get')
        def output_item(id, create_date, title, val):
            return (id, create_date, title, val)

        dt = datetime.now()

        self.assertEqual(output_item(id=1, create_date=dt, title='test', val={'a': 1}), (1, dt, 'test', {'a': 1}))

        self.assertEqual(output_item(id=1, create_date=dt, title='test', val={'a': 1}), (1, dt, 'test', {'a': 1}))

        with self.assertRaises(AttributeError):
            output_item(id='1', create_date=dt, title='test', val={'a': 1})

        with self.assertRaises(AttributeError):
            output_item(id=1, create_date=None, title='test', val={'a': 1})

        with self.assertRaises(AttributeError):
            output_item(id=1, create_date=dt, title={'a': '1'}, val={'a': 1})

        with self.assertRaises(AttributeError):
            output_item(id=1, create_date=dt, title='test', val={1, 2, 3})

        with self.assertRaises(AttributeError):
            output_item(id=None, create_date=None, title=None, val=None)


    def test_multiple_args_ignored_args(self):
        """Testing multiple arguments when some arguments are not specified in decorator"""

        @self.check_arg_attrs(a='copy', b='month', d='imag')
        def output_item(a, b, c, d):
            return (a, b, c, d)

        dt = datetime.now()

        self.assertEqual(output_item(a=[1, 2], b=dt, c='test', d=1), ([1, 2], dt, 'test', 1))

        self.assertEqual(output_item(a=[1, 2], b=dt, c=1, d=1), ([1, 2], dt, 1, 1))

        self.assertEqual(output_item(a=[1, 2], b=dt, c=None, d=1.5), ([1, 2], dt, None, 1.5))

        with self.assertRaises(AttributeError):
            output_item(a='1', b=dt, c='test', d=1)

        with self.assertRaises(AttributeError):
            output_item(a=1, b=None, c='test', d=1)

        with self.assertRaises(AttributeError):
            output_item(a=1, b=dt, c='test', d=Decimal('-1.3'))

        with self.assertRaises(AttributeError):
            output_item(a=None, b=None, c=None, d=None)


    def test_common_attrs(self):
        """Test to ensure that types with similar attributes all match"""

        class CustomClass():
            def pop(self):
                return 'pop!'

        @self.check_arg_attrs(a='pop')
        def return_values(a, b):
            return (a, b)

        cstm = CustomClass()

        self.assertEqual(return_values(a=[1, 2, 3], b=0), ([1, 2, 3], 0))

        self.assertEqual(return_values(a={1, 2, 3}, b=0), ({1, 2, 3}, 0))

        self.assertEqual(return_values(a={'a': 1, 'b': 2, 'c': 3}, b=0), ({'a': 1, 'b': 2, 'c': 3}, 0))

        self.assertEqual(return_values(a=cstm, b=0), (cstm, 0))
