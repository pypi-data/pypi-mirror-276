from setuptools import setup, find_packages

setup(
    name='BrainSliceClassifier',
    version='1.2.2',
    packages=find_packages(),
    install_requires=[
        'torchvision',
        'torch',
        'scikit-learn',
        'tqdm',
        'numpy',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'BrainSliceClassifier = BrainSliceClassifier.BrainSliceClassifier:main'
        ],
    },
    author='Wei-Chun Kevin Tsai',
    author_email='coachweichun@gmail.com',
    description='The Python package provides tools for classifying the specified brain slices based on the Cholinergic Pathways HyperIntensities Scale.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='All Rights Reserved',
)