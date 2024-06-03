from setuptools import find_packages, setup

setup(
    name='rl-test-task-2',
    version='0.1.5',
    description='Task 2',
    author='Antonio Corluka',
    author_email='antonio.corluka@outlook.com',
    packages=find_packages(),
    python_requires='>=3.11',
    install_requires=[
        'rl-test-common',
        'rl-test-storage-handlers'
    ]
)
