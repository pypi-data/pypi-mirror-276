from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "aixhello.xyello",
        ["aixhello/xyello.pyx"],
    )
]

cythonize_options = {
    'compiler_directives': {
        'language_level': 3,         
        'emit_code_comments': False,  
    }
}

setup(
    name='aixhello',
    version='3.2',  # Increment the version number
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
    install_requires=[
        'requests',  
        'cryptography',
        'openai',
    ],
    ext_modules=cythonize(extensions, **cythonize_options),
    packages=['aixhello'],
)