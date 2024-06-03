from setuptools import setup, find_packages

setup(
    name='balanco_library',
    version='0.1.1',
    author='Elias Isopahkala',
    author_email='elias.isopahkala@balanco.fi',
    description='A simple example package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/balanco-elias/balanco_library',  # Update with your repo URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

