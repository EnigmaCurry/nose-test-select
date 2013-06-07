Nose-Test-Select
========

nose-test-select is a
[Nose](http://somethingaboutorange.com/mrl/projects/nose) plugin that
provides a more convenient method of selecting (including and excluding)
tests than the built-in regex methods. Tests are selected by creating a
file similar to a .gitignore file.

Example Config
==============

Assume we have a project directory that looks like the following:

```
.
├── my_module
├── setup.py
└── tests
    ├── math_tests.py
    ├── network_tests.py
    ├── not_working
    │   ├── a.py
    │   └── b.py
    └── vector_tests.py
```

A test selection config file might look like:

```
[exclude]
math_tests.py:*Integer*
tests/not_working/*

[include]
tests/not_working/a.py:ATest.oneWorkingMethod
```

This config file will run all tests except for the methods in
```math_tests.py``` that have 'Integer' in their name, and none of the
modules found in the ```not_working``` directory except for a single
method in ```a.py``` called ```ATest.oneWorkingMethod```. If
specifying the method name, you must include the class name or a ```*```.


Tests that match any pattern in the ```[include]``` section will
always be run. Any other test that matches any pattern in the
```[exclude]``` section will not be run. Tests that don't match
either section will be run. If you want to exclude all tests by
default, you need a config like:

```
# Exclude all tests by default:
[exclude]
*

[include]
# Include all the vector tests:
tests/vector_tests.py
# Include all the math test methods that end in 'Float':
tests/math_tests.py:*Float
```

Lines starting with a ```#``` symbol are treated as comments.

Note: Tests must still follow the regular nose naming convention. 
Tests that don't follow this convention will be ignored even if 
they match a pattern in your config file. You can redefine the 
regular nose test match pattern by specifying ```--testmatch```

Running
=======

Once you have your config file created you run nose like so:

```
nosetests --test-select-config=my_config.cfg
```

or

```
export NOSE_TEST_SELECT_CONFIG=/path/to/my_config.cfg
nosetests
```
