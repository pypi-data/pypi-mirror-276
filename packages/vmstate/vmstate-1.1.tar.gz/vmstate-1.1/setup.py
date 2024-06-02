from setuptools import setup, find_packages

setup(
    name='vmstate',  # Replace with your package name
    version='1.1',
    packages=find_packages(),  # Automatically find and include packages
    author='Ashish Sangra',
    author_email='your.email@example.com',
    description='A brief description of your package',
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
