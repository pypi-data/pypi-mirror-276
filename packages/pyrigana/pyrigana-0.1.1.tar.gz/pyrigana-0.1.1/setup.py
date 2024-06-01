from setuptools import setup, find_packages

setup(
    name='pyrigana',
    version='0.1.1',
    description='A brief description of my package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aknay/pyrigana',
    author='Nay Aung Kyaw',
    author_email='aknay@outlook.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'jaconv',
        'fugashi',
        'fugashi[unidic-lite]'
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
