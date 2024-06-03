from setuptools import setup, find_packages

setup(
    name='minisklearn',
    version='0.1.3',
    author='Ayman Youss & Amine Idrissi',
    author_email='ayman.youss@um6p.ma',
    description='Mini Scikit Learn',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AymanYouss/mini-scikit-learn',  # Replace with your repository URL
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scipy'
    ],
)
