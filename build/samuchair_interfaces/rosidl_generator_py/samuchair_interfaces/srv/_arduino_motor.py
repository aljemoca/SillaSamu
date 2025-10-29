# generated from rosidl_generator_py/resource/_idl.py.em
# with input from samuchair_interfaces:srv/ArduinoMotor.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ArduinoMotor_Request(type):
    """Metaclass of message 'ArduinoMotor_Request'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('samuchair_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'samuchair_interfaces.srv.ArduinoMotor_Request')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__arduino_motor__request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__arduino_motor__request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__arduino_motor__request
            cls._TYPE_SUPPORT = module.type_support_msg__srv__arduino_motor__request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__arduino_motor__request

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ArduinoMotor_Request(metaclass=Metaclass_ArduinoMotor_Request):
    """Message class 'ArduinoMotor_Request'."""

    __slots__ = [
        '_command',
        '_x',
        '_y',
    ]

    _fields_and_field_types = {
        'command': 'string',
        'x': 'uint8',
        'y': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.command = kwargs.get('command', str())
        self.x = kwargs.get('x', int())
        self.y = kwargs.get('y', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.command != other.command:
            return False
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def command(self):
        """Message field 'command'."""
        return self._command

    @command.setter
    def command(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'command' field must be of type 'str'"
        self._command = value

    @builtins.property
    def x(self):
        """Message field 'x'."""
        return self._x

    @x.setter
    def x(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'x' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'x' field must be an unsigned integer in [0, 255]"
        self._x = value

    @builtins.property
    def y(self):
        """Message field 'y'."""
        return self._y

    @y.setter
    def y(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'y' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'y' field must be an unsigned integer in [0, 255]"
        self._y = value


# Import statements for member types

# already imported above
# import builtins

# already imported above
# import rosidl_parser.definition


class Metaclass_ArduinoMotor_Response(type):
    """Metaclass of message 'ArduinoMotor_Response'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('samuchair_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'samuchair_interfaces.srv.ArduinoMotor_Response')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__srv__arduino_motor__response
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__srv__arduino_motor__response
            cls._CONVERT_TO_PY = module.convert_to_py_msg__srv__arduino_motor__response
            cls._TYPE_SUPPORT = module.type_support_msg__srv__arduino_motor__response
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__srv__arduino_motor__response

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ArduinoMotor_Response(metaclass=Metaclass_ArduinoMotor_Response):
    """Message class 'ArduinoMotor_Response'."""

    __slots__ = [
        '_status',
        '_out',
        '_x',
        '_y',
    ]

    _fields_and_field_types = {
        'status': 'boolean',
        'out': 'string',
        'x': 'uint8',
        'y': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.status = kwargs.get('status', bool())
        self.out = kwargs.get('out', str())
        self.x = kwargs.get('x', int())
        self.y = kwargs.get('y', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.status != other.status:
            return False
        if self.out != other.out:
            return False
        if self.x != other.x:
            return False
        if self.y != other.y:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def status(self):
        """Message field 'status'."""
        return self._status

    @status.setter
    def status(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'status' field must be of type 'bool'"
        self._status = value

    @builtins.property
    def out(self):
        """Message field 'out'."""
        return self._out

    @out.setter
    def out(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'out' field must be of type 'str'"
        self._out = value

    @builtins.property
    def x(self):
        """Message field 'x'."""
        return self._x

    @x.setter
    def x(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'x' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'x' field must be an unsigned integer in [0, 255]"
        self._x = value

    @builtins.property
    def y(self):
        """Message field 'y'."""
        return self._y

    @y.setter
    def y(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'y' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'y' field must be an unsigned integer in [0, 255]"
        self._y = value


class Metaclass_ArduinoMotor(type):
    """Metaclass of service 'ArduinoMotor'."""

    _TYPE_SUPPORT = None

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('samuchair_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'samuchair_interfaces.srv.ArduinoMotor')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._TYPE_SUPPORT = module.type_support_srv__srv__arduino_motor

            from samuchair_interfaces.srv import _arduino_motor
            if _arduino_motor.Metaclass_ArduinoMotor_Request._TYPE_SUPPORT is None:
                _arduino_motor.Metaclass_ArduinoMotor_Request.__import_type_support__()
            if _arduino_motor.Metaclass_ArduinoMotor_Response._TYPE_SUPPORT is None:
                _arduino_motor.Metaclass_ArduinoMotor_Response.__import_type_support__()


class ArduinoMotor(metaclass=Metaclass_ArduinoMotor):
    from samuchair_interfaces.srv._arduino_motor import ArduinoMotor_Request as Request
    from samuchair_interfaces.srv._arduino_motor import ArduinoMotor_Response as Response

    def __init__(self):
        raise NotImplementedError('Service classes can not be instantiated')
