#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This file is released under BSD 2-clause license.
import codecs
import datetime
import os
import subprocess
import click as click
from slugify import slugify
from clicks import cli
import config
from helpers import group_iterate, pad_string, DateParamType
from manager import PostManager, posts

__author__ = 'ipwx'


@cli.group()
def post():
    pass


@post.command()
@click.option('--count', '-n', help='Maximum count of tags to output.',
              default=10, type=int)
def tags(count):
    """Query about the recent tags."""
    tags = PostManager(os.path.join(config.BLOG_ROOT, '_posts')).getTags()
    for tag_group in group_iterate(tags[:count], 5):
        print(''.join(pad_string(s, 20) for s in tag_group))


@post.command()
@click.option('--count', '-n', help='Maximum count of tags to output.',
              default=10, type=int)
def categories(count):
    """Query about the recent tags."""
    categories = posts.getCategories()
    for cate_group in group_iterate(categories[:count], 5):
        print(''.join(pad_string(s, 20) for s in cate_group))


@post.command()
@click.option('--title', '-t', help='Specify the title of the new post.',
              type=click.STRING)
@click.option('--name', '-n', help='Specify the name of the new post.',
              type=click.STRING)
@click.option('--subtitle', '-S', help='Specify the subtitle of the new post.',
              type=click.STRING)
@click.option('--date', '-d', help='Specify the date of the new post.',
              type=DateParamType())
@click.option('--author', '-a', help='Specify the author of the new post.',
              type=click.STRING)
@click.option('--category', '-c', help='Specify the category of the new post.',
              type=click.STRING)
@click.option('--tag', '-T', help='Specify the tags of the new post.',
              multiple=True, type=click.STRING)
@click.option('--overwrite', '-o', help='Overwrite existing file.',
              default=False, type=click.BOOL, is_flag=True)
@click.option('--open', '-O', 'open_new_file', default=True, type=click.BOOL,
              help='Open the new file after creation.')
def new(title, name, subtitle=None, date=None, author=None, category=None,
        tag=None, overwrite=False, open_new_file=True):
    if not title:
        raise Exception("Title must not be empty.")
    if not name:
        name = slugify(title)
    if not author:
        author = '平芜泫'
    if date is None:
        date = datetime.datetime.now()
    if category is None:
        category = '未分类'
    tags = tag if tag else None
    file_name = '_posts/%s-%s.md' % (date.strftime('%Y-%m-%d'), name)
    path = os.path.join(config.BLOG_ROOT, file_name)
    if os.path.isfile(path):
        if not overwrite and not click.confirm('Overwrite %s?' % file_name):
            return

    contents = [
        '---',
        'layout:        post',
        'title:         %s' % title,
    ]
    if subtitle:
        contents.append('subtitle:      %s' % subtitle)
    contents += [
        'author:        %s' % author,
        'category:      %s' % category,
        'date:          %s' % date.strftime('%Y-%m-%d %H:%M:%S'),
    ]
    if tags:
        contents.append('tags:')
        for t in tag:
            contents.append('    - %s' % t)
    contents += ['---', '']

    with codecs.open(path, 'wb', 'utf-8') as f:
        f.write('\n'.join(contents))

    print('Created %s' % file_name)
    if open_new_file:
        subprocess.check_call(['open', path])


@post.command()
def list():
    """List posts."""
    for name in posts.listPosts():
        print(name)


@post.command()
@click.option('--date', '-d', help='Specify the date of post to be deleted.',
              type=DateParamType(), multiple=True)
@click.option('--latest', '-L', help='Delete the latest post.',
              default=False, type=click.BOOL, is_flag=True)
def delete(date, latest):
    """Delete specified posts."""
    names = posts.listPosts()
    if latest and names:
        if click.confirm('Delete %s?' % names[0]):
            posts.deleteFile(names[0])
            print('* %s deleted.' % names[0])
            names = names[1:]
    if date and names:
        for name in names:
            if any(name.startswith(d.strftime('%Y-%m-%d')) for d in date):
                if click.confirm('Delete %s?' % name):
                    posts.deleteFile(name)
                    print('* %s deleted.' % name)