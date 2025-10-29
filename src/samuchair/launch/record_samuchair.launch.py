from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os
from datetime import datetime

def generate_launch_description():
    # Ruta al launch principal de SamuChair
    samuchair_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('samuchair'),
                'launch',
                'samuchair.launch.py'
            )
        )
    )
    # Generar timestamp: YYYYMMDD_HHMMSS
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Nombre del bag con timestamp
    bag_name = f"./samuchair_bag/{timestamp}"
    # Comando para grabar todos los tópicos después de 5 segundos
    rosbag_record = ExecuteProcess(
        cmd=['ros2', 'bag', 'record', '-a', '-o', bag_name],
        output='screen'
    )

    delayed_rosbag = TimerAction(
        period=5.0,  # segundos de espera
        actions=[rosbag_record]
    )

    return LaunchDescription([
        samuchair_launch,
        delayed_rosbag
    ])
