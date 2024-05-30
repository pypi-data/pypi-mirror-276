from setuptools import setup, find_packages

setup(
    name='myfunctions_farrukh90',
    version='0.0.10',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/farrukh90/',
    license='MIT',
    author='Farrukh Sadykov',
    author_email='farrukhsadykov@gmail.com',
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
