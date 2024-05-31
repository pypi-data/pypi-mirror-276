from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='roxCrypter',
    version='1.0.1',
    description='A custom encryption package for blank text & passwords',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Samet Karapınar',
    author_email='skrpnr4@gmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
    url='https://github.com/sametkarapinar/roxCrypter',
    project_urls={
        'Source': 'https://github.com/sametkarapinar/roxCrypter',
    },
)
