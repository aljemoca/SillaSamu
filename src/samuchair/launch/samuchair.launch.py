from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, TimerAction


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='samuchair',
            executable='esp32Node',
            name='sensorHallyPot'
        ),
        Node(
            package='samuchair',
            executable='arduinoNode',
            name='Joystick'
        ),
        Node(
            package='samuchair',
            executable='testArduinoNode',
            name='testJoystick'
        ),

        Node(
            package='samuchair',
            executable='webcamNode',
            name='webcam'
        ),
        Node(
            package='samuchair',
            executable='secondarytaskNode',
            name='ST'
        ),  
        Node(
            package='samuchair',
            executable='tactilesNode',
            name='tactiles'
        ),
        
        # Puedes añadir nodos adicionales aquí
    ])
