
from setuptools import setup, find_packages

setup(
    name='arion_library',
    version='1.1rc107.dev107',  
    author='Heni Nechi',  
    author_email='h.nechi@arion-tech.com',  
    url='https://github.com/Ariontech/ArionLibrary.git',  
    packages=find_packages(),  
    python_requires='>=3.8',  
    install_requires=['pyodbc', 'pytest', 'pytest', 'responses', 'pysftp==0.2.9', 'ShopifyAPI==12.5.0', 'requests==2.31.0', 'pytest'],
)