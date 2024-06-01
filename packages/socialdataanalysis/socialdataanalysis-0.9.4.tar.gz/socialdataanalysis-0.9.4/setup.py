from setuptools import setup, find_packages

setup(
    name='socialdataanalysis',
    version='0.9.4',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'socialdataanalysis': ['socialdataanalysis/notebooks/*.ipynb'],
    },
    install_requires=[
        'pandas',
        'numpy',
        'statsmodels',
        'scipy',
        'matplotlib',
        'sympy',
        'prince',
        'altair',
        'pyreadstat'
    ],
    author='Ricardo Mergulhao',
    author_email='ricardomergulhao@gmail.com',
    description='Funções personalizadas para análise de dados nas ciências sociais, complementando o uso do SPSS.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rcmergulhao/socialdataanalysis',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
