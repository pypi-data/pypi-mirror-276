from setuptools import setup, find_packages

setup(
    name='color_mapper',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
    ],
    description='A package for normalizing values and mapping them to a color gradient.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/psymoniko/color_mapper',
    author='Ali Mohammadnia',
    author_email='alimohammadnia127@example.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
