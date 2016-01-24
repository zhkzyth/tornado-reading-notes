#!/usr/bin/env python
# encoding: utf-8

"""Implementation of platform-specific functionality.

For each function or class described in `tornado.platform.interface`,
the appropriate platform-specific implementation exists in this module.
Most code that needs access to this functionality should do e.g.::

    from tornado.platform.auto import set_close_exec
"""

from __future__ import absolute_import, division, print_function, with_statement

import os

if os.name == 'nt':
    from tornado.platform.common import Waker
    from tornado.platform.windows import set_close_exec
else:
    from tornado.platform.posix import set_close_exec, Waker

try:
    # monotime monkey-patches the time module to have a monotonic function
    # in versions of python before 3.3.
    import monotime
except ImportError:
    pass
try:
    from time import monotonic as monotonic_time
except ImportError:
    monotonic_time = None
