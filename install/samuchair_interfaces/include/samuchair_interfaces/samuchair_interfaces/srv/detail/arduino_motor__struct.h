// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from samuchair_interfaces:srv/ArduinoMotor.idl
// generated code does not contain a copyright notice

#ifndef SAMUCHAIR_INTERFACES__SRV__DETAIL__ARDUINO_MOTOR__STRUCT_H_
#define SAMUCHAIR_INTERFACES__SRV__DETAIL__ARDUINO_MOTOR__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'command'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ArduinoMotor in the package samuchair_interfaces.
typedef struct samuchair_interfaces__srv__ArduinoMotor_Request
{
  rosidl_runtime_c__String command;
  uint8_t x;
  uint8_t y;
} samuchair_interfaces__srv__ArduinoMotor_Request;

// Struct for a sequence of samuchair_interfaces__srv__ArduinoMotor_Request.
typedef struct samuchair_interfaces__srv__ArduinoMotor_Request__Sequence
{
  samuchair_interfaces__srv__ArduinoMotor_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} samuchair_interfaces__srv__ArduinoMotor_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'out'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/ArduinoMotor in the package samuchair_interfaces.
typedef struct samuchair_interfaces__srv__ArduinoMotor_Response
{
  bool status;
  rosidl_runtime_c__String out;
  uint8_t x;
  uint8_t y;
} samuchair_interfaces__srv__ArduinoMotor_Response;

// Struct for a sequence of samuchair_interfaces__srv__ArduinoMotor_Response.
typedef struct samuchair_interfaces__srv__ArduinoMotor_Response__Sequence
{
  samuchair_interfaces__srv__ArduinoMotor_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} samuchair_interfaces__srv__ArduinoMotor_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SAMUCHAIR_INTERFACES__SRV__DETAIL__ARDUINO_MOTOR__STRUCT_H_
