pydep 0.0.1 : Release Notes
=============
A python object dependency graph generator

This is a simple python AST walker. It walks the AST to determines the references to an object/method of a class from other classes in the file provided.

You can try

`python parser.py X sample ./sample.py`

The following output is produced

`+  X_sample:
+  fn_using_y_getX_sample:./sample.py:31
     getX_y_Y:./sample.py:23,./sample.py:24
     +  somefunc_referer_sample:./sample.py:11
     +  somefunc_sample:./sample.py:7,./sample.py:8
`

Dependencies
=============

pip install logilab-astng


Browsing the generated dependency graph
========================================

    1. Open that file in emacs. Add file-clickable.el and enable that mode for the file.
    2. From each line in file , click Ctrl-X[ and that should take you to another window with the corresponding file opened and at the appropriate line.


Caveats
=======
- The application has been tested with only some of the python project I have worked on. Not battle tested!
- Performance:
    - Need to cache infer operation of astng, so that the parser does not take too. Currently, the parser may slow dow for large code bases.
