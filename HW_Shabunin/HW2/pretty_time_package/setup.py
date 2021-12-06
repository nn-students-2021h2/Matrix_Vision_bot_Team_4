from setuptools import setup

setup(
    name='pretty_print_package',
    version='0.1',
    description='description',
    url='http://github.com/name/package_name',
    author='VlaDick',
    author_email='shabunin.vladislav@mail.ru',   #Он рабоает с .ru?
    license='MIT',
    namespace_packages=['name'],
    packages=['name.pretty_print_package'],
    install_requires=[
        'requests==2.26.0',
    ],
)