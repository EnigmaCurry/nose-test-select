from setuptools import setup

VERSION = '0.1'

setup(
    name = "nose-test-select",
    version = VERSION,
    author = "Ryan McGuire",
    author_email = "ryan@enigmacurry.com",
    description = ".gitignore style test selection for nose (file and method name globbing)",
    license = 'MIT',
    url = "http://github.com/EnigmaCurry/nose-test-select",
    packages = ['nose_test_select'],
    zip_safe = False,    
    entry_points = {
        'nose.plugins': ['nose_test_select = nose_test_select.nose_test_select:NoseTestSelect']
        },
    classifiers = [
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires = ['nose'],
    test_suite='tests'
)
