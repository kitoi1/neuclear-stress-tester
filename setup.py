
from setuptools import setup, find_packages

setup(
    name='ultimate-nuclear-stress-tester',
    version='4.0',
    description='💣 Ultimate Stress Tester for Developers – Python Edition by Kasau',
    author='Kasau',
    author_email='kasaufx@gmail.com',
    packages=find_packages(include=['core']),
    include_package_data=True,
    install_requires=[
        'requests',
        'colorama'
    ],
    entry_points={
        'console_scripts': [
            'unst=main:main_menu'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Load Testing'
    ],
    python_requires='>=3.6'
)
