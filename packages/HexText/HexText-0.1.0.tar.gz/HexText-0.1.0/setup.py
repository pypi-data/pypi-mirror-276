from setuptools import setup, find_packages

setup(
    name='HexText',
    version='0.1.0',
    author='ZakRehman',
    author_email='zaksteryt@gmail.com',
    description='Create Coloured/Gradient Text In Python',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SirScripter/HexText',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
