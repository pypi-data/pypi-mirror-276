from setuptools import setup, find_packages

setup(
    name='lcprogramtools',
    version='0.0.51',
    description='A demo Python package which does nothing really right now',
    author='Subham Sarangi',
    author_email='ivan.sarangi@email.com',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'greetme=lcprogramtools.module:main',
        ],
    },
)
