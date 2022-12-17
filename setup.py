from setuptools import setup
import os
from glob import glob

package_name = 'neato_autorace'

config_module = "neato_autorace/config"
config_main_module = "config"
detection_module ="neato_autorace/Detection"
detection_lanes_module ="neato_autorace/Detection/Lanes"

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name, 
              detection_lanes_module, 
              detection_module, config_module,
              config_main_module],
              
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name,'launch'), glob('launch/*')),
        (os.path.join('lib', package_name), glob('scripts/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='abdulla',
    maintainer_email='abdll1@hotmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'computer_vision_node = neato_autorace.computer_vision_node:main',
        ],
    },
)

