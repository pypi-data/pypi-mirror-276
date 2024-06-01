from setuptools import setup, find_packages

setup(
    name='lcprogramtools',
    version='0.0.3',
    description='A demo Python package',
    author='Your Name',
    author_email='your@email.com',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'greet=lcprogramtools.module:main',
        ],
    },
)
