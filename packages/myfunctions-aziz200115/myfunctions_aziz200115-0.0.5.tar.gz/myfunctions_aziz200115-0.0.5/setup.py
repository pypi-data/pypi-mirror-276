from setuptools import setup, find_packages

setup(
    name='myfunctions_aziz200115',
    version='0.0.5',
    packages=find_packages(),
    install_requires=["os"],
    url='https://github.com/aziz200115/',
    license='MIT',
    author='Aziz Shekerbekov',
    author_email='awekerbekov@gmail.com',
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