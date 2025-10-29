// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from samuchair_interfaces:srv/ArduinoMotor.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "samuchair_interfaces/srv/detail/arduino_motor__rosidl_typesupport_introspection_c.h"
#include "samuchair_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "samuchair_interfaces/srv/detail/arduino_motor__functions.h"
#include "samuchair_interfaces/srv/detail/arduino_motor__struct.h"


// Include directives for member types
// Member `command`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  samuchair_interfaces__srv__ArduinoMotor_Request__init(message_memory);
}

void samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_fini_function(void * message_memory)
{
  samuchair_interfaces__srv__ArduinoMotor_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_message_member_array[3] = {
  {
    "command",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(samuchair_interfaces__srv__ArduinoMotor_Request, command),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(samuchair_interfaces__srv__ArduinoMotor_Request, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(samuchair_interfaces__srv__ArduinoMotor_Request, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_message_members = {
  "samuchair_interfaces__srv",  // message namespace
  "ArduinoMotor_Request",  // message name
  3,  // number of fields
  sizeof(samuchair_interfaces__srv__ArduinoMotor_Request),
  samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_message_member_array,  // message members
  samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_message_type_support_handle = {
  0,
  &samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_samuchair_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, samuchair_interfaces, srv, ArduinoMotor_Request)() {
  if (!samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_message_type_support_handle.typesupport_identifier) {
    samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &samuchair_interfaces__srv__ArduinoMotor_Request__rosidl_typesupport_introspection_c__ArduinoMotor_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "samuchair_interfaces/srv/detail/arduino_motor__rosidl_typesupport_introspection_c.h"
// already included above
// #include "samuchair_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "samuchair_interfaces/srv/detail/arduino_motor__functions.h"
// already included above
// #include "samuchair_interfaces/srv/detail/arduino_motor__struct.h"


// Include directives for member types
// Member `out`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  samuchair_interfaces__srv__ArduinoMotor_Response__init(message_memory);
}

void samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_fini_function(void * message_memory)
{
  samuchair_interfaces__srv__ArduinoMotor_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_message_member_array[4] = {
  {
    "status",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(samuchair_interfaces__srv__ArduinoMotor_Response, status),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "out",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(samuchair_interfaces__srv__ArduinoMotor_Response, out),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(samuchair_interfaces__srv__ArduinoMotor_Response, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(samuchair_interfaces__srv__ArduinoMotor_Response, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_message_members = {
  "samuchair_interfaces__srv",  // message namespace
  "ArduinoMotor_Response",  // message name
  4,  // number of fields
  sizeof(samuchair_interfaces__srv__ArduinoMotor_Response),
  samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_message_member_array,  // message members
  samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_message_type_support_handle = {
  0,
  &samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_samuchair_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, samuchair_interfaces, srv, ArduinoMotor_Response)() {
  if (!samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_message_type_support_handle.typesupport_identifier) {
    samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &samuchair_interfaces__srv__ArduinoMotor_Response__rosidl_typesupport_introspection_c__ArduinoMotor_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "samuchair_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "samuchair_interfaces/srv/detail/arduino_motor__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers samuchair_interfaces__srv__detail__arduino_motor__rosidl_typesupport_introspection_c__ArduinoMotor_service_members = {
  "samuchair_interfaces__srv",  // service namespace
  "ArduinoMotor",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // samuchair_interfaces__srv__detail__arduino_motor__rosidl_typesupport_introspection_c__ArduinoMotor_Request_message_type_support_handle,
  NULL  // response message
  // samuchair_interfaces__srv__detail__arduino_motor__rosidl_typesupport_introspection_c__ArduinoMotor_Response_message_type_support_handle
};

static rosidl_service_type_support_t samuchair_interfaces__srv__detail__arduino_motor__rosidl_typesupport_introspection_c__ArduinoMotor_service_type_support_handle = {
  0,
  &samuchair_interfaces__srv__detail__arduino_motor__rosidl_typesupport_introspection_c__ArduinoMotor_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, samuchair_interfaces, srv, ArduinoMotor_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, samuchair_interfaces, srv, ArduinoMotor_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_samuchair_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, samuchair_interfaces, srv, ArduinoMotor)() {
  if (!samuchair_interfaces__srv__detail__arduino_motor__rosidl_typesupport_introspection_c__ArduinoMotor_service_type_support_handle.typesupport_identifier) {
    samuchair_interfaces__srv__detail__arduino_motor__rosidl_typesupport_introspection_c__ArduinoMotor_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)samuchair_interfaces__srv__detail__arduino_motor__rosidl_typesupport_introspection_c__ArduinoMotor_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, samuchair_interfaces, srv, ArduinoMotor_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, samuchair_interfaces, srv, ArduinoMotor_Response)()->data;
  }

  return &samuchair_interfaces__srv__detail__arduino_motor__rosidl_typesupport_introspection_c__ArduinoMotor_service_type_support_handle;
}
