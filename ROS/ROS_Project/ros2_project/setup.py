from setuptools import setup
import os
from glob import glob


package_name = 'ros2_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='moha',
    maintainer_email='mohamedabdelwahabb96@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'control_node = ros2_project.control_node:main',
        'spawn_node = ros2_project.spawn_node:main',
        ],
    },
)
