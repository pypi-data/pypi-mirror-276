from setuptools import find_packages, setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='dre4my_detection',
    version='0.1.3',
    packages=find_packages(include=['anomaly_detection_methods', 'anomaly_detection_methods.*']),
    include_package_data=True,
    package_data={
        'dre4my_detection': [
            'ML_BASED/logistic_regression_model.pkl',
            'ML_BASED/tfidf_vectorizer.pkl',
            'SIGNATURE_BASED/signatures.json',
        ],
    },    description='Library for detecting abnormal HTTP-packets using one of the methods listed below.',
    author='Dre4my',
    install_requires=['certifi==2024.2.2', 'cffi==1.16.0', 'charset-normalizer==3.3.2', 
                    'cryptography==42.0.7', 'docutils==0.21.2', 'idna==3.7', 
                    'importlib_metadata==7.1.0', 'jaraco.classes==3.4.0', 'jaraco.context==5.3.0', 
                    'jaraco.functools==4.0.1', 'jeepney==0.8.0', 'joblib==1.4.2', 
                    'keyring==25.2.1', 'markdown-it-py==3.0.0', 'mdurl==0.1.2', 
                    'more-itertools==10.2.0', 'nh3==0.2.17', 'numpy==1.26.4', 
                    'pandas==2.2.2', 'pkginfo==1.10.0', 'pycparser==2.22', 
                    'Pygments==2.18.0', 'python-dateutil==2.9.0.post0', 'pytz==2024.1', 
                    'readme_renderer==43.0', 'requests==2.32.2', 'requests-toolbelt==1.0.0', 
                    'rfc3986==2.0.0', 'rich==13.7.1', 'scikit-learn==1.5.0', 
                    'scipy==1.13.1', 'SecretStorage==3.3.3', 'setuptools==70.0.0', 
                    'six==1.16.0', 'threadpoolctl==3.5.0', 'twine==5.1.0', 
                    'tzdata==2024.1', 'urllib3==2.2.1', 'wheel==0.43.0', 'zipp==3.18.2'],
    setup_requires=['certifi==2024.2.2', 'cffi==1.16.0', 'charset-normalizer==3.3.2', 
                    'cryptography==42.0.7', 'docutils==0.21.2', 'idna==3.7', 
                    'importlib_metadata==7.1.0', 'jaraco.classes==3.4.0', 'jaraco.context==5.3.0', 
                    'jaraco.functools==4.0.1', 'jeepney==0.8.0', 'joblib==1.4.2', 
                    'keyring==25.2.1', 'markdown-it-py==3.0.0', 'mdurl==0.1.2', 
                    'more-itertools==10.2.0', 'nh3==0.2.17', 'numpy==1.26.4', 
                    'pandas==2.2.2', 'pkginfo==1.10.0', 'pycparser==2.22', 
                    'Pygments==2.18.0', 'python-dateutil==2.9.0.post0', 'pytz==2024.1', 
                    'readme_renderer==43.0', 'requests==2.32.2', 'requests-toolbelt==1.0.0', 
                    'rfc3986==2.0.0', 'rich==13.7.1', 'scikit-learn==1.5.0', 
                    'scipy==1.13.1', 'SecretStorage==3.3.3', 'setuptools==70.0.0', 
                    'six==1.16.0', 'threadpoolctl==3.5.0', 'twine==5.1.0', 
                    'tzdata==2024.1', 'urllib3==2.2.1', 'wheel==0.43.0', 'zipp==3.18.2'],
    long_description=long_description,
    long_description_content_type="text/markdown",
)