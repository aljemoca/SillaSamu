from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, TimerAction


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='samuchair',
            executable='movilNode',
            name='Movil'
        ),
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
        #Node(
         #   package='samuchair',
          #  executable='testArduinoNode',
           # name='testJoystick'
        #),
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
        Node(
            package='samuchair',
            executable='jBNode',
            name='JoystickBluetooth'
        ),
        Node(
            package='samuchair',
            executable='mainNode',
            name='mainNode'
        ),
        Node(
            package='samuchair',
            executable='opasistidaNode',
            name='opasistidaNode'
        ),
        Node(
            package='samuchair',
            executable='alarmNode',
            name='alarmNode'
        ),
        Node(
            package='samuchair',
            executable='BagControlNode',
            name = 'BagControlNode'
        ),
        Node(
            package='samuchair',
            executable='loggerNode',
            name = 'loggerNode'
        ),
        
        # Puedes añadir nodos adicionales aquí
    ])
