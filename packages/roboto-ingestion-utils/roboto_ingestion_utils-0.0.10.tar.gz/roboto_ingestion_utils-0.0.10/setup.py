from setuptools import setup, find_packages

setup(
    name='roboto_ingestion_utils',
    version='0.0.10',
    author='Roboto Technologies',
    author_email='yves@roboto.ai',
    description='Utility functions for roboto data ingestion',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/roboto-ai/roboto-ingestion-utils',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        # List your dependencies here
    ],
)
