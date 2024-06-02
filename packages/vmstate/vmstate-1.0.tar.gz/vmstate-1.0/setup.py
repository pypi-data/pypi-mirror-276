from setuptools import setup, find_packages

setup(
    name='vmstate',
    version='1.0',
    packages=find_packages(),
    author='Ashish Sangra',
    author_email='ashishsangra42@gmail.com',
    description='get virtual machine information azure sub module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/asangra127/openPackages/raw/main/README.md',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
