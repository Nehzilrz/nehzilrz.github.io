#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This file is released under BSD 2-clause license.

from __future__ import unicode_literals

import os
import datetime
import shutil
import yaml
import config


class PostManager(object):

    def __init__(self, post_root):
        self.post_root = post_root

    def tryLoadMeta(self, filePath):
        """Try to load the meta data from filePath."""
        with open(filePath, 'rb') as f:
            firstLine = f.readline()
            if firstLine and firstLine.rstrip() == b'---':
                header = []
                line = None
                for line in f:
                    line = line.rstrip()
                    if line == b'---':
                        break
                    header.append(line)
                if line != b'---':
                    return
                header = b'\n'.join(header)
                try:
                    return yaml.load(header)
                except Exception:
                    return

    def getTags(self):
        """Get tag list according to MRU order."""
        tags = {}
        names = sorted(os.listdir(self.post_root), reverse=True)
        for idx, name in enumerate(names):
            meta = self.tryLoadMeta(os.path.join(self.post_root, name))
            if meta and meta['tags'] and isinstance(meta['tags'], list):
                for t in meta['tags']:
                    tags.setdefault(t, 0)
                    tags[t] += (len(names) - idx)
        return sorted(tags.keys(), key=lambda k: (-tags[k], k))

    def getCategories(self):
        """Get category list according to MRU order."""
        categories = {}
        names = sorted(os.listdir(self.post_root), reverse=True)
        for idx, name in enumerate(names):
            meta = self.tryLoadMeta(os.path.join(self.post_root, name))
            if meta and meta['category']:
                c = meta['category']
                categories.setdefault(c, 0)
                categories[c] += 1
        return sorted(categories.keys(), key=lambda k: (-categories[k], k))

    def listPosts(self):
        """List names of posts."""
        names = sorted(os.listdir(self.post_root), reverse=True)
        ret = []
        for name in names:
            if self.tryLoadMeta(os.path.join(self.post_root, name)) is not None:
                ret.append(name)
        return ret

    def deleteFile(self, name):
        os.remove(os.path.join(self.post_root, name))


class UploadManager(object):
    """Manages uploaded static files."""

    def __init__(self, upload_root):
        self.upload_root = upload_root

    def addFile(self, name, sourceFile):
        name = '%s/%s' % (datetime.datetime.now().strftime('%Y/%m'), name)
        mainName, extName = os.path.splitext(name)
        retry = 1
        dstPath = None
        while True:
            dstPath = os.path.join(self.upload_root, name)
            if not os.path.exists(dstPath):
                break
            name = '%s-%d%s' % (mainName, retry, extName)
            retry += 1
        dstDir = os.path.split(dstPath)[0]
        if not os.path.isdir(dstDir):
            os.makedirs(dstDir)
        shutil.copyfile(sourceFile, dstPath)
        return name

    def deleteFile(self, name):
        target = os.path.join(self.upload_root, name)
        targetDir = os.path.split(target)[0]
        os.remove(target)
        try:
            os.removedirs(targetDir)
        except Exception:
            pass


posts = PostManager(os.path.join(config.BLOG_ROOT, '_posts'))
uploads = UploadManager(os.path.join(config.BLOG_ROOT, 'upload'))
