from setuptools import setup, find_packages

setup(
    name='game',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'unittest-mock'
    ],
    entry_points={
        'console_scripts': [
            'run_game_tests=test_game:main',
        ],
    },
)
