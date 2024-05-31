from setuptools import setup, find_packages

setup(
    name='yfunc',
    version='1.0.0',
    description='a collection of some productive functions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='yzjsswk',
    author_email='yzjsswk@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=[],
)
