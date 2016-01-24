#!/usr/bin/env python
# encoding: utf-8

"""EPoll-based IOLoop implementation for Linux systems."""
from __future__ import absolute_import, division, print_function, with_statement

import select

from tornado.ioloop import PollIOLoop


class EPollIOLoop(PollIOLoop):
    def initialize(self, **kwargs):
        super(EPollIOLoop, self).initialize(impl=select.epoll(), **kwargs)
