import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'ShehrozAli_launch_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Includes all launch files
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shehbot',
    maintainer_email='shehbot@todo.todo',
    description='Follow the leader turtle simulation',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # This allows you to run: ros2 run ShehrozAli_launch_pkg follower_node
            'follower_node = ShehrozAli_launch_pkg.turtlesim_followleader_node:main',
        ],
    },
)
