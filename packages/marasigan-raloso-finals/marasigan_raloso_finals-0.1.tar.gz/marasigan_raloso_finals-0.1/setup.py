from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='marasigan_raloso_finals',
    version='0.1',
    packages=find_packages(),
    description='Inventory Management System',
    author='John Aron Marasigan, John Paul Raloso',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=description,
    long_description_content_type='text/markdown',
)