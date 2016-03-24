Author: yuchao

Last modified: 2016-03-23 17:32

Filename: readme.md

Description: python daemon scripts.

Usage:

    python main.py [start|stop|restart]

    add scripts [test_method.py] into d/modules/.

    edit d/call.py, add [import d.modules.test_method].
    statement variables from [d.modules.test_method].
    append task functions into class CallLoop().__alarm() or CallLoop().__info().

