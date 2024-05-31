from setuptools import setup, find_packages

setup(
    name='chakhalyan',
    version='0.1.0',
    author='Professor',
    author_email='test@harevan.ru',
    description='A simple example package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/chakhalyan',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.2',
)