from setuptools import setup, find_packages

setup(
    name='omnijp',
    version='2.7.0',
    packages=find_packages(),
    install_requires=[
        'retry>=0.9.2',
        'requests>=2.31.0',
        'pymssql>=2.3.0',
        'psycopg2>=2.9.9',
        'openai~=1.30.5'
    ],
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here
        ],
    },
    # Additional metadata
    author='Jessish Pothancheri',
    author_email='jessish.pothancheri@gmail.com',
    description='OmniJP is a Python library that provides tools for common tasks in software development',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jpothanc/omnijp',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',],
    python_requires='>=3.8',
)
