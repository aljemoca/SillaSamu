// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from samuchair_interfaces:srv/ArduinoMotor.idl
// generated code does not contain a copyright notice

#ifndef SAMUCHAIR_INTERFACES__SRV__DETAIL__ARDUINO_MOTOR__BUILDER_HPP_
#define SAMUCHAIR_INTERFACES__SRV__DETAIL__ARDUINO_MOTOR__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "samuchair_interfaces/srv/detail/arduino_motor__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace samuchair_interfaces
{

namespace srv
{

namespace builder
{

class Init_ArduinoMotor_Request_y
{
public:
  explicit Init_ArduinoMotor_Request_y(::samuchair_interfaces::srv::ArduinoMotor_Request & msg)
  : msg_(msg)
  {}
  ::samuchair_interfaces::srv::ArduinoMotor_Request y(::samuchair_interfaces::srv::ArduinoMotor_Request::_y_type arg)
  {
    msg_.y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::samuchair_interfaces::srv::ArduinoMotor_Request msg_;
};

class Init_ArduinoMotor_Request_x
{
public:
  explicit Init_ArduinoMotor_Request_x(::samuchair_interfaces::srv::ArduinoMotor_Request & msg)
  : msg_(msg)
  {}
  Init_ArduinoMotor_Request_y x(::samuchair_interfaces::srv::ArduinoMotor_Request::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_ArduinoMotor_Request_y(msg_);
  }

private:
  ::samuchair_interfaces::srv::ArduinoMotor_Request msg_;
};

class Init_ArduinoMotor_Request_command
{
public:
  Init_ArduinoMotor_Request_command()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ArduinoMotor_Request_x command(::samuchair_interfaces::srv::ArduinoMotor_Request::_command_type arg)
  {
    msg_.command = std::move(arg);
    return Init_ArduinoMotor_Request_x(msg_);
  }

private:
  ::samuchair_interfaces::srv::ArduinoMotor_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::samuchair_interfaces::srv::ArduinoMotor_Request>()
{
  return samuchair_interfaces::srv::builder::Init_ArduinoMotor_Request_command();
}

}  // namespace samuchair_interfaces


namespace samuchair_interfaces
{

namespace srv
{

namespace builder
{

class Init_ArduinoMotor_Response_y
{
public:
  explicit Init_ArduinoMotor_Response_y(::samuchair_interfaces::srv::ArduinoMotor_Response & msg)
  : msg_(msg)
  {}
  ::samuchair_interfaces::srv::ArduinoMotor_Response y(::samuchair_interfaces::srv::ArduinoMotor_Response::_y_type arg)
  {
    msg_.y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::samuchair_interfaces::srv::ArduinoMotor_Response msg_;
};

class Init_ArduinoMotor_Response_x
{
public:
  explicit Init_ArduinoMotor_Response_x(::samuchair_interfaces::srv::ArduinoMotor_Response & msg)
  : msg_(msg)
  {}
  Init_ArduinoMotor_Response_y x(::samuchair_interfaces::srv::ArduinoMotor_Response::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_ArduinoMotor_Response_y(msg_);
  }

private:
  ::samuchair_interfaces::srv::ArduinoMotor_Response msg_;
};

class Init_ArduinoMotor_Response_out
{
public:
  explicit Init_ArduinoMotor_Response_out(::samuchair_interfaces::srv::ArduinoMotor_Response & msg)
  : msg_(msg)
  {}
  Init_ArduinoMotor_Response_x out(::samuchair_interfaces::srv::ArduinoMotor_Response::_out_type arg)
  {
    msg_.out = std::move(arg);
    return Init_ArduinoMotor_Response_x(msg_);
  }

private:
  ::samuchair_interfaces::srv::ArduinoMotor_Response msg_;
};

class Init_ArduinoMotor_Response_status
{
public:
  Init_ArduinoMotor_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ArduinoMotor_Response_out status(::samuchair_interfaces::srv::ArduinoMotor_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_ArduinoMotor_Response_out(msg_);
  }

private:
  ::samuchair_interfaces::srv::ArduinoMotor_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::samuchair_interfaces::srv::ArduinoMotor_Response>()
{
  return samuchair_interfaces::srv::builder::Init_ArduinoMotor_Response_status();
}

}  // namespace samuchair_interfaces

#endif  // SAMUCHAIR_INTERFACES__SRV__DETAIL__ARDUINO_MOTOR__BUILDER_HPP_
