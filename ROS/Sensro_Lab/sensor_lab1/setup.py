from setuptools import setup

package_name = 'sensor_lab1'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
        'task1 = sensor_lab1.task1:main',
        'task2 = sensor_lab1.task2:main'
        ],
    },
)
