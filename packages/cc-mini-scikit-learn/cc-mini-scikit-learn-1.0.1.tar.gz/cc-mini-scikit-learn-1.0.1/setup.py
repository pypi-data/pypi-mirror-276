from setuptools import setup, find_packages

setup(
    name='cc-mini-scikit-learn',
    version='1.0.1',
    author='basma-arnaoui',
    author_email='basma.arnaoui@um6p.ma',
    description='A mini implementation of Scikit-Learn with custom models and metrics',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.18.0',
        'scipy>=1.4.0',
        'scikit-learn>=0.22.0',
        'matplotlib>=3.1.0',
    ],
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md'],
    },
   
)
