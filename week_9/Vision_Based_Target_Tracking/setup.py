from setuptools import find_packages, setup

package_name = 'Vision_Based_Target_Tracking'

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
    maintainer_email='ranashehrozali2@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'tracking_node = Vision_Based_Target_Tracking.tracking_node:main',
        'multiple_tracking_node = Vision_Based_Target_Tracking.multiple_tracking_node:main',
       ],
    },
)
