from setuptools import setup, find_packages

setup(
    name='myfunctions_AdnanGrifat',
    version='0.0.16',
    packages=find_packages(),
    install_requires=["os"],
    url='https://github.com/AdnanGrifat/',
    license='MIT',
    author='Adnan Grifat',
    author_email='grifat1978@gmail.com',
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