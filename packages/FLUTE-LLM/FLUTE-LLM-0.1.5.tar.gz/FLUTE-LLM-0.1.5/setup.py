from setuptools import setup, find_packages

setup(
    name='FLUTE-LLM',
    version='0.1.5',
    description='A package for prompt processing and language model interaction',
    author='The Pioneer',
    url='https://github.com/thepioneerjp/FLUTE',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'openai',
        'anthropic',
        'google-generativeai',
        'python-dotenv',
        'pytest',
    ],
    package_data={
        '': ['*.txt', '*.md', '*.json', '*.csv', '*.yaml', '*.yml', "LICENSE"],
        'flute': ['**/*'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)