#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This file is released under BSD 2-clause license.
from click import ParamType
import dateutil.parser

import six
import sys


def group_iterate(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i+batch_size]


def pad_string(s, width):
    w = 0
    if not isinstance(s, six.text_type):
        s = six.text_type(s, 'utf-8')
    for c in s:
        if ord(c) > 127:
            w += 2
        else:
            w += 1
    if w >= width:
        return s
    return s + (' ' * (width - w))


class DateParamType(ParamType):
    name = 'date'

    def convert(self, value, param, ctx):
        if isinstance(value, bytes):
            try:
                enc = getattr(sys.stdin, 'encoding', None)
                if enc is not None:
                    value = value.decode(enc)
            except UnicodeError:
                try:
                    value = value.decode(sys.getfilesystemencoding())
                except UnicodeError:
                    value = value.decode('utf-8', 'replace')
            ret = value
        else:
            ret = value
        return dateutil.parser.parse(ret)

    def __repr__(self):
        return 'DATE'
