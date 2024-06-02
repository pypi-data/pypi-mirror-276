from setuptools import setup, find_packages

setup(
    name='teammate',
    version='0.0.0',
    author='Teammate Pte. Ltd.',
    author_email='hello@teammate.ltd',
    description='The official python library for Teammate AI Services.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8, <4',
)
