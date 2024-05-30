from setuptools import setup, find_packages

setup(
    name='DNAPROT',
    version='0.1.0',
    description='A DNA and protein analyser tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Juan Salafranca, Marie Van Rossum',
    author_email='juan.salafrancamartinez@epfl.ch , marie.vanrossum@epfl.ch',
    url='https://github.com/juan-salafranca/Project-Dna',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pandas',
        'openpyxl',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)