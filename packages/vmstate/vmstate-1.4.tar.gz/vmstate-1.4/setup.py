from setuptools import setup, find_packages

print(find_packages())

setup(
    name='vmstate',  # Replace with your package name
    version='1.4',  # Increment the version number
    #packages=find_packages(),  # Automatically find and include packages
    packages=['vmstate','computeclient'],
    author='Ashish Sangra',
    author_email='ashishsangra42@gmail.com',
    install_requires=[
        'azure-identity',
        'azure-mgmt-compute',
    ],
    description='submodule for azure virtual machines info',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_package',  # Replace with your package URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
