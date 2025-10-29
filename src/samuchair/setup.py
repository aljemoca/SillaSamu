from setuptools import find_packages, setup
import os
from glob import glob



package_name = 'samuchair'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
         # Esta línea es la importante
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][y|m]'))),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='labserver',
    maintainer_email='labserver@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['esp32Node = samuchair.esp32Node:main',
                            'webcamNode = samuchair.webcamNode:main',
                            'secondarytaskNode = samuchair.secondarytaskNode:main',
                            'arduinoNode=samuchair.arduinoNode:main',
                            'testArduinoNode=samuchair.testArduinoNode:main',
                            'movilNode=samuchair.movilNode:main',
                            'tactilesNode=samuchair.tactilesNode:main',
        ],
    },
)
