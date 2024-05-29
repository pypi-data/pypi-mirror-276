from setuptools import setup, find_packages

setup(
    name='bluffpaddingcypher',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='BluffPadding Cipher Algorithm: A Python-based encryption tool combining random prefixes/suffixes with character shifts for enhanced text obfuscation.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Bhavya Padaliya',
    url='https://github.com/neuqs90/bluffpadding-cypher-algorithm.git',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Security :: Cryptography',
    ],
    keywords='encryption, cipher, obfuscation, security',
    python_requires='>=3.6',
    py_modules=['cypher'],
    package_dir={'bluffpaddingcypher': 'bluffpaddingcypher'},
)
