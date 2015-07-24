#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This file is released under BSD 2-clause license.
import os
import click as click
from clicks import cli
from manager import uploads

__author__ = 'ipwx'


@cli.group()
def upload():
    pass


@upload.command()
@click.argument('source', nargs=-1, type=click.Path(exists=True))
def add(source):
    for src in source:
        name = os.path.split(src)[1]
        dst = uploads.addFile(name, src)
        print('*  Src:  %s' % src)
        print('   Dest: %s' % dst)


@upload.command()
@click.argument('name', nargs=1, type=click.Path())
def delete(name):
    uploads.deleteFile(name)
    print('%s deleted.' % name)
