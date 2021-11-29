from setuptools import setup


setup(
    name='get_time_package',
    version='0.1',
    description='description',
    url='http://github.com/name/package_name',
    author='Egor Sysoev',
    author_email='email@example.com',
    license='MIT',
    namespace_packages=['get_time_namespace'],
    packages=['get_time_namespace.get_time_unicode_packages'],


    install_requires=[
        'requests==2.26.0',
    ],
entry_points={
        'console_scripts': [
            'get_time=get_time_namespace.get_time_unicode_packages.get_time_unicode_module:main',
        ]
    }
    )