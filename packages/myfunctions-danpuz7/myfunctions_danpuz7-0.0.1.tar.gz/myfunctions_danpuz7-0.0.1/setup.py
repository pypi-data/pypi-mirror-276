from setuptools import setup, find_packages

setup(
    name='myfunctions_danpuz7',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/danpuz7',
    license='MIT',
    author='Daniel Puzan',
    author_email='danpuz7@gmail.com',
    description='A description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)