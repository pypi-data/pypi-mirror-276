from setuptools import setup, find_packages

setup(
    name='mem-client',
    version='0.0.2',
    description='A brief description of your package',
    author='Jaro Uljanovs',
    author_email='jaro@aiforall.dev',
    url='https://github.com/ElviiAi/mem-client',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'python-dotenv>=0.19.2',
        'click>=8.0.3',
    ],
    entry_points={
        'console_scripts': [
            'mem-client=cli:main',
        ],
    },
)