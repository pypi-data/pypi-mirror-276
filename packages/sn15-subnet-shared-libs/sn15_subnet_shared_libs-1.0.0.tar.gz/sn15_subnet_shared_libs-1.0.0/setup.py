from setuptools import setup, find_packages

setup(
    name='sn15_subnet_shared_libs',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        'pydantic',
        'bittensor',
    ],
    author='Dmytro Savenkov',
    author_email='dmytro.savenkov@chain-insights.ai',
    description='All shared libs that all components, executables, and services of Sn15 are based on',
    url='https://github.com/YOUR_USERNAME/YOUR_REPOSITORY',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
