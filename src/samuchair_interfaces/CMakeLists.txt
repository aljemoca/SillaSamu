cmake_minimum_required(VERSION 3.8)
project(samuchair_interfaces)

# Necesario para cualquier paquete ROS 2
find_package(ament_cmake REQUIRED)

# Para generar mensajes y servicios
find_package(rosidl_default_generators REQUIRED)

# Generación de servicios
rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/ArduinoMotor.srv"
)

# Exportar runtime de ROSIDL (clave para Python)
ament_export_dependencies(rosidl_default_runtime)

# Finalizar el paquete
ament_package()

