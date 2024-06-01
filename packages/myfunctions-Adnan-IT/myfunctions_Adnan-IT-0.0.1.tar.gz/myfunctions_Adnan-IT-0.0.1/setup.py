from setuptools import setup, find_packages

setup(
    name='myfunctions_Adnan-IT',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/Adnan-IT',
    license='MIT',
    author='Adnan-IT',
    author_email='adnan123it@gmail.com',
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
