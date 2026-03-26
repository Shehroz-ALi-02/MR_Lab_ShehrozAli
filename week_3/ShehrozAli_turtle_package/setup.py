from setuptools import find_packages, setup

package_name = 'ShehrozAli_turtle_package'

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
            'my_node = ShehrozAli_turtle_package.my_node:main',
            'move_turtle = ShehrozAli_turtle_package.move_turtle:main',
            'move_circle = ShehrozAli_turtle_package.move_circle:main',
       	    'move_triangle = ShehrozAli_turtle_package.move_triangle:main',
       	    'move_spawn = ShehrozAli_turtle_package.move_turtle_spawn:main',
       	    'move_p2p = ShehrozAli_turtle_package.move_turtle_specific_point:main'
        ],
    },
)
