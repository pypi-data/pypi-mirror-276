from setuptools import setup, find_packages

setup(
    name='rxnSMILES4AtomEco',
    version='1.0.4',
    packages=find_packages(),
    description='Calculate atom economy for chemical reactions using reaction SMILES',
    author='Samuele Giani',
    author_email='samuele.giani@empa.ch',
    url='https://pypi.org/project/rxnSMILES4AtomEco/1.0.0/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
