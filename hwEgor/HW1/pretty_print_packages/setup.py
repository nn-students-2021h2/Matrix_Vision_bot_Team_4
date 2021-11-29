from setuptools import setup


setup(
    name='pretty_print_package',
    version='0.1',
    description='description',
    url='http://github.com/name/package_name',
    author='Egor Sysoev',
    author_email='email@example.com',
    license='MIT',
    namespace_packages=['get_time_namespace2'],
    packages=['get_time_namespace2.get_time_packages'],
    install_requires=[
        'requests==2.26.0',
        ],

entry_points={
        'console_scripts': [
            'get_time=get_time_namespace2.get_time_packages.get_time_pp_module:main',
        ]
    }
    )