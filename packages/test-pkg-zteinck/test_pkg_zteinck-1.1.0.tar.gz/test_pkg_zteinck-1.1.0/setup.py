from setuptools import find_packages, setup

setup(
    name='test_pkg_zteinck',
    packages=find_packages(),
    version='1.1.0',
    description='test package',
    author='Zachary Einck',
    # license='MIT',
    install_requires=[
        'requests',
        ],
    )