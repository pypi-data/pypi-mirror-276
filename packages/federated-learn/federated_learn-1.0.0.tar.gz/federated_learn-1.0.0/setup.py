from setuptools import setup, find_packages

setup(
    name='federated_learn',
    version='1.0.0',
    author='Md. Golam Mostofa',
    author_email='mostofa@devolvedai.com',
    packages=find_packages(),

    install_requires=[
        'numpy==1.26.4',
        'torch==2.3.0',
        'tiktoken==0.7.0',

    ],

    # entry_points={
    #     'console_scripts': [
    #         'fyes=federated_learning_installed:main_function',  # Correct format for entry point
    #     ],
    # },
)
