from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.readlines()
    
setup(
    install_requires=read_requirements(),
    name='GnosisTech',
    version='1.0.2',
    author='Phung Ngoc An',
    author_email='phungankh2@gmail.com',
    description='PyQuantTrader là một thư viện Python hỗ trợ những vấn đề về quant trading.',
    packages=find_packages(),
    package_data= {'pyquanttrade': ['_backtest_source/*.js']},       
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    python_requires='>=3.6',
)