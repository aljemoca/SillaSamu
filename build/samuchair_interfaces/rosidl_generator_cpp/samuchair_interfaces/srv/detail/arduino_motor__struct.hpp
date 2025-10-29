// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from samuchair_interfaces:srv/ArduinoMotor.idl
// generated code does not contain a copyright notice

#ifndef SAMUCHAIR_INTERFACES__SRV__DETAIL__ARDUINO_MOTOR__STRUCT_HPP_
#define SAMUCHAIR_INTERFACES__SRV__DETAIL__ARDUINO_MOTOR__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__samuchair_interfaces__srv__ArduinoMotor_Request __attribute__((deprecated))
#else
# define DEPRECATED__samuchair_interfaces__srv__ArduinoMotor_Request __declspec(deprecated)
#endif

namespace samuchair_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ArduinoMotor_Request_
{
  using Type = ArduinoMotor_Request_<ContainerAllocator>;

  explicit ArduinoMotor_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command = "";
      this->x = 0;
      this->y = 0;
    }
  }

  explicit ArduinoMotor_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : command(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->command = "";
      this->x = 0;
      this->y = 0;
    }
  }

  // field types and members
  using _command_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _command_type command;
  using _x_type =
    uint8_t;
  _x_type x;
  using _y_type =
    uint8_t;
  _y_type y;

  // setters for named parameter idiom
  Type & set__command(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->command = _arg;
    return *this;
  }
  Type & set__x(
    const uint8_t & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const uint8_t & _arg)
  {
    this->y = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__samuchair_interfaces__srv__ArduinoMotor_Request
    std::shared_ptr<samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__samuchair_interfaces__srv__ArduinoMotor_Request
    std::shared_ptr<samuchair_interfaces::srv::ArduinoMotor_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ArduinoMotor_Request_ & other) const
  {
    if (this->command != other.command) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    return true;
  }
  bool operator!=(const ArduinoMotor_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ArduinoMotor_Request_

// alias to use template instance with default allocator
using ArduinoMotor_Request =
  samuchair_interfaces::srv::ArduinoMotor_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace samuchair_interfaces


#ifndef _WIN32
# define DEPRECATED__samuchair_interfaces__srv__ArduinoMotor_Response __attribute__((deprecated))
#else
# define DEPRECATED__samuchair_interfaces__srv__ArduinoMotor_Response __declspec(deprecated)
#endif

namespace samuchair_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct ArduinoMotor_Response_
{
  using Type = ArduinoMotor_Response_<ContainerAllocator>;

  explicit ArduinoMotor_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = false;
      this->out = "";
      this->x = 0;
      this->y = 0;
    }
  }

  explicit ArduinoMotor_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : out(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = false;
      this->out = "";
      this->x = 0;
      this->y = 0;
    }
  }

  // field types and members
  using _status_type =
    bool;
  _status_type status;
  using _out_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _out_type out;
  using _x_type =
    uint8_t;
  _x_type x;
  using _y_type =
    uint8_t;
  _y_type y;

  // setters for named parameter idiom
  Type & set__status(
    const bool & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__out(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->out = _arg;
    return *this;
  }
  Type & set__x(
    const uint8_t & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const uint8_t & _arg)
  {
    this->y = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__samuchair_interfaces__srv__ArduinoMotor_Response
    std::shared_ptr<samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__samuchair_interfaces__srv__ArduinoMotor_Response
    std::shared_ptr<samuchair_interfaces::srv::ArduinoMotor_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ArduinoMotor_Response_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->out != other.out) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    return true;
  }
  bool operator!=(const ArduinoMotor_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ArduinoMotor_Response_

// alias to use template instance with default allocator
using ArduinoMotor_Response =
  samuchair_interfaces::srv::ArduinoMotor_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace samuchair_interfaces

namespace samuchair_interfaces
{

namespace srv
{

struct ArduinoMotor
{
  using Request = samuchair_interfaces::srv::ArduinoMotor_Request;
  using Response = samuchair_interfaces::srv::ArduinoMotor_Response;
};

}  // namespace srv

}  // namespace samuchair_interfaces

#endif  // SAMUCHAIR_INTERFACES__SRV__DETAIL__ARDUINO_MOTOR__STRUCT_HPP_
