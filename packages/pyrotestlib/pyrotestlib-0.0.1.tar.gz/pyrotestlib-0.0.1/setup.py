from setuptools import setup, find_packages

__version__ = "0.0.1"

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

if __name__ == "__main__":
    setup(
        name='pyrotestlib',
        version=__version__,
        long_description=readme,
        long_description_content_type='text/markdown',
        description='Python package for a test',
        author='Pyro-Maniac',
        author_email='mgarrixx04@gmail.com',
        url='https://github.com/mgarrixx/pyrotestlib',
        install_requires=['distlib', 'idna'],
        packages=find_packages(exclude=[]),
        keywords=['embedded', 'log collector'],
        python_requires='>=3.6',
    )