from setuptools import setup, find_packages

setup(
    name='professordriver',
    version='0.1.0',
    author='Hovhannes',
    author_email='test@harevan.ru',
    description='A utility package to set up Selenium WebDriver with custom configurations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/professordriver',
    packages=find_packages(),
    package_data={'professordriver': ['data/*.crx']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'selenium>=3.141.0',
    ],
)