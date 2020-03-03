from setuptools import setup, find_packages

setup(
    name='python',
    version='0.0.1',
    packages=find_packages(),
    python_requires='>=3.5',
    install_requires=[
        'requests',
    ],
    entry_points = {
        'console_scripts': [
            'pyexample=pyexample.__main__:main',
        ],
    }
)
