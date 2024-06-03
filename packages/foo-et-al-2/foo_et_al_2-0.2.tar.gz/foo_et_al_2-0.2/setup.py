from setuptools import setup, find_packages

setup(
    name='foo_et_al_2',
    version='0.2',
    author='Joseph Willem Ricci',
    author_email='josephwillemricci@gmail.com',
    description='A python package for the Foo et al. parameterization, et al.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[],
)