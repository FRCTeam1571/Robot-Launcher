from setuptools import setup
setup(
    name='robotpy launcher',
    entry_points={
        'console_scripts': [
            'launch=launcher:run'
        ]
    }
)
