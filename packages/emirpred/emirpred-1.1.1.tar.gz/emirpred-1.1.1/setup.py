from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='emirpred',
    version='1.1.1',
    description='A tool to predict exosomal miRNA',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/emirpred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'emirpred.':['**/*'], 
    'emirpred.blast_db':['**/*'],
    'emirpred.model':['*'],
    'emirpred.MERCI':['*'],
    'emirpred.data':['*'],
    'emirpred.output':['*'],
    'emirpred.Standalone_Nfeature':['*'],
    },

    entry_points={ 'console_scripts' : ['emirpred = emirpred.python_scripts.emirpred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas', 'scikit-learn==1.2.2','joblib','argparse' # Add any Python dependencies here
        ],
    extras_require={ "dev":["pytest>=7.0", "twine>=4.0.2"]

    }

)
