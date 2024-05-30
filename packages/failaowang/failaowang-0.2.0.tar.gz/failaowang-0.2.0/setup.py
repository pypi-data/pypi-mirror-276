from setuptools import setup, find_packages

setup(
    name='failaowang',
    version='0.2.0',
    packages=find_packages(),
    url='https://github.com/yourusername/your_project',
    license='MIT',
    author='laowang',
    author_email='931417425@qq.com',
    description='A short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        # List your package dependencies here
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
