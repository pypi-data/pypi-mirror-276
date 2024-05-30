from setuptools import setup, find_packages

setup(
    name='myfunctions_SashaKrav',
    version='0.0.13',
    packages=find_packages(),
    install_requires=[],
    url='https://github.com/SashaKrav',
    license='MIT',
    author='SashaKrav',
    author_email='kravcov4k@gmail.com',
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