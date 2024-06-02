"""A setup module for patternlib."""


from setuptools import find_packages, setup
from code import patternlib


LONG_DESCRIPTION = """
 Pattern Library contains generic patterns that can be printed by invoking the pattern methods.
"""

setup(
    name='patternlib',
    # also update the version in patternlib.__init__.py file
    version=patternlib.VERSION,
    description='Pattern Library in Python',
    long_description=LONG_DESCRIPTION,
    license = "BSD",
    # The project's main homepage.
    url='https://github.com/gautamkhanapuri/patternlib.git',
    author='Gautam AK',
    author_email='gautamajey@gmail.com',
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "License :: OSI Approved :: BSD License",
    ],
    packages=find_packages(where="code", exclude=[]),
    package_dir={'': 'code'},
    setup_requires=[],
    install_requires=[],
    python_requires='>=3.0',
)

