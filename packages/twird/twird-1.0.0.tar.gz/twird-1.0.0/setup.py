from setuptools import setup, find_packages

setup(
    name='twird',
    version='1.0.0',
    description='A Discord bot language made in python',
    author='Siddhartha41210',
    author_email='siddharthab41210@gmail.com',
    url='https://github.com/twizzers01/twird',
    packages=find_packages(),
    install_requires=[
        'discord.py>=2.0.0'
    ],
    python_requires='>=3.6',
)
