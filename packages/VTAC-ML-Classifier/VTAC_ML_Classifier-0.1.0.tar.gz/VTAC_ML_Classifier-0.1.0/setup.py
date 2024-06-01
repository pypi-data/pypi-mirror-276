from setuptools import setup, find_packages

setup(
    name='VTAC_ML_Classifier',
    version='0.1.0',
    packages=find_packages(include=['testing', 'testing.*']),
    install_requires=[
        # List your dependencies here
        # Example: 'numpy', 'pandas', 'scikit-learn',
    ],
    entry_points={
        'console_scripts': [
            # Define any command-line scripts here
            # Example: 'vtac_classifier=pipeline:main',
        ],
    },
    url='https://github.com/yourusername/VTAC_ML_Classifier',  # Replace with your project's URL
    license='MIT',
    author='Your Name',
    author_email='your.email@example.com',
    description='A short description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
