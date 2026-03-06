
from setuptools import find_packages, setup

package_name = 'ShehrozAli_first_pkg'

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
		'simple_node = ShehrozAli_first_pkg.simple_node:main',
		'simple_node1 = ShehrozAli_first_pkg.simple_node1:main',		  
      ],
    },
)
