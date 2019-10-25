#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import os

import util

def relative_file_read(calling_file, relative_file):
    return os.path.join(os.path.dirname(calling_file), *relative_file)

