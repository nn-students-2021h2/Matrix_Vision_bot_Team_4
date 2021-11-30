from setuptools import setup


setup(
    namespace_packages=['time_package'],
    name='get_time_package',
    version='0.1',
    description='description',
    url='http://github.com/name/package_name',
    author='Anastasia Polina',
    author_email='email@example.com',
    license='MIT',
    packages=['time_package.get_time_package'],
    install_requires=[
        'requests==2.26.0',
    ],
    entry_points={
            'console_scripts': [
            'get_time=time_package.get_time_package.get_time_module:main',
        ]
    }
)
