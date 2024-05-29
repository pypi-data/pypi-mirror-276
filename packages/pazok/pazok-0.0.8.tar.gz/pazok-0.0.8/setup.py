from setuptools import setup, find_packages

setup(
    name='pazok',
    version='0.0.8',
    author='b_azo',
    author_email='husseun.selt@gmail.com',
    description='A short description of my package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
