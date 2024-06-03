from setuptools import setup, find_packages

setup(
    name='mini_scikit_learn',  # Replace with your package name
    version='0.1.3',  # Initial version of your package
    author='Yassir Fri',
    author_email='your.email@example.com',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/YASSIRFRI/mini_scikit_learn.git",
    packages=find_packages(),  
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
