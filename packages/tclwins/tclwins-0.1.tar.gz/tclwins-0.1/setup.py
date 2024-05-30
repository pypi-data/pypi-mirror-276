from setuptools import setup, find_packages

setup(
    name='tclwins',
    version='0.1',
    author='Sion',
    author_email='the.rckr@gmail.com',
    description='My version of Tcl/Tk bindings for Python',
    packages=find_packages(),
    install_requires=[
        'tkinter'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
