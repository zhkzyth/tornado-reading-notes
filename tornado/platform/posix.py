#!/usr/bin/env python
# encoding: utf-8

"""Posix implementations of platform-specific functionality."""

from __future__ import absolute_import, division, print_function, with_statement

import fcntl
import os

from tornado.platform import interface


def set_close_exec(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFD)
    fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)


def _set_nonblocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)


class Waker(interface.Waker):
    def __init__(self):
        r, w = os.pipe()
        _set_nonblocking(r)
        _set_nonblocking(w)
        set_close_exec(r)
        set_close_exec(w)
        self.reader = os.fdopen(r, "rb", 0)
        self.writer = os.fdopen(w, "wb", 0)

    def fileno(self):
        return self.reader.fileno()

    def write_fileno(self):
        return self.writer.fileno()

    def wake(self):
        try:
            self.writer.write(b"x")
        except IOError:
            pass

    def consume(self):
        try:
            while True:
                result = self.reader.read()
                if not result:
                    break
        except IOError:
            pass

    def close(self):
        self.reader.close()
        self.writer.close()
