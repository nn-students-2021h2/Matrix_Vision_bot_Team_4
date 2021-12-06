from setuptools import setup

setup(
    name='get_time_package',
    version='0.1',
    description='description',
    url='http://github.com/name/package_name',
    author='VlaDick',
    author_email='shabunin.vladislav@mail.ru',   #Он рабоает с .ru?
    license='MIT',
    namespace_packages=['name'],
    packages=['name.get_time_package'],
    entry_points={
        'console_scripts': [
            'get_time=name.get_time_package.get_time_module:main'
        ]
    }
)