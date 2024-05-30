from setuptools import setup, find_packages

setup(
    name='chars',
    version='0.1.2',
    packages=find_packages(),
    description='A package for character sets',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='PiyushThePal',
    author_email='cool_guy2331708@yahoo.com',
    # url='https://github.com/yourusername/mypackage',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
