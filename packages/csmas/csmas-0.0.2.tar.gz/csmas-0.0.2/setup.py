from setuptools import setup

setup(
    long_description="""This is a simple programm to get updates of server's status on Discord""",
    name='csmas',
    version='0.0.2',
    packages=['csmas'],
    entry_points={
        'console_scripts': [
            'csmas=your_package.__init__:main',
        ],
    },
)
