from setuptools import setup, find_packages
import os

# Utility function to read the README file.
# Used for the long_description. It's nice to have this in the setup file so
# that the distribution will have a more comprehensive description.
def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup(
    name='static-analysis-script',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Perzibel',
    author_email='perzibel@outlook.com',
    description='A utility to perform static analysis on files.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',  # This is important for rendering Markdown from README
    url='https://github.com/perzibel/static-analysis-script',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'analysis=analysis.main:main',
        ],
    },
    install_requires=[
        'PyPDF2',
        'tqdm',
        'numpy',
        'pyfiglet',
        'colorama',
        'setuptools_scm'
    ],
    include_package_data=True,
    package_data={
        "analysis": ["../bin/strings.exe"],  # Make sure the path matches your structure
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
