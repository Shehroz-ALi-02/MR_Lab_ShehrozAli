from setuptools import find_packages, setup

package_name = 'ShehrozAli_Gazebo_Rviz_nvg_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='shehbot',
    maintainer_email='shehbot@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'cmd_vel_publisher_node = ShehrozAli_Gazebo_Rviz_nvg_pkg.cmd_vel_publisher_node:main',
        'odom_subscriber_node = ShehrozAli_Gazebo_Rviz_nvg_pkg.odom_subscriber_node:main',
        ],
    },
)
