from setuptools import setup, find_packages

setup(
    name='sktlearn_clone',
    version='0.2.0',
    description='A custom implementation of various machine learning algorithms and utilities inspired by Scikit-Learn',
    author='Ilyas Boudhaine & Zineb Abercha',
    author_email='ilyasboudhaine1@gmail.com, zineb03abercha@gmail.com',
    url='https://github.com/iboud0/scikit_learn_clone',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scipy',
        'scikit-learn',
    ],
)
