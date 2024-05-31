from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name='aixhello',
    version='1.2',
    description='AI HRM Package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='SecureAI',
    author_email='package@xerocai.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    ext_modules=cythonize([Extension("aixhello.xyello", ["aixhello/xyello.pyx"])]),
    packages=['aixhello'],
)
