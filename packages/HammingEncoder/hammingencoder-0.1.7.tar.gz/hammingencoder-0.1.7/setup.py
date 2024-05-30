from setuptools import setup, find_packages

setup(
    name='HammingEncoder',
    version='0.1.7',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'torch',
        'scikit-learn',
        'pandas',
        'tqdm'
    ],
    description='A Hamming Encoder package',
    long_description=open('README.md').read(),
    # long_description_content_type='text/x-rst',
    long_description_content_type='text/markdown',
    author='Junjie Dong',
    author_email='jd445@qq.com',
    url='https://github.com/jd445/HammingEncoder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
