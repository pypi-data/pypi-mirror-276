from setuptools import setup, find_packages

setup(
    name='NeuroKit_Eda_Analaysis',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'neurokit2',
        'scipy'
    ],
    author='Mohammad Saquib Daiyan',
    author_email='shadmanshahin6@gmail.com',
    description='A library for processing and analyzing EDA signals.',
    url='https://github.com/saquib34/NeuroKit_Eda_Analaysis',
    classifiers=[
'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
],
python_requires='>=3.11',
)
