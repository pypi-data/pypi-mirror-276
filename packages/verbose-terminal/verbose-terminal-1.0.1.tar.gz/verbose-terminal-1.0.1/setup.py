from setuptools import setup, find_packages

setup(
    name='verbose-terminal',
    version='1.0.1',
    author='Wipodev',
    author_email='ajwipo@gmail.com',
    description='A Python library for displaying messages in the terminal with styles and logging support.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wipodev/Verbose_Terminal',
    project_urls={
        'Documentation': 'https://github.com/wipodev/Verbose_Terminal/blob/main/README.md',
        'Source': 'https://github.com/wipodev/Verbose_Terminal',
        'Bug Tracker': 'https://github.com/wipodev/Verbose_Terminal/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    license='MIT',
    keywords='python, terminal, console, verbose, verbose terminal, verbose terminal, verbose terminal',
    packages=find_packages(exclude=('tests*', 'testing*', 'test*')),
)