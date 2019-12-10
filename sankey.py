#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
python bokeh interface with the JS D3-sankey library and "actual code"
"""

import os
import bokeh.core.properties as bk_properties
import bokeh.models as bk_models

import util


class Sankey(bk_models.LayoutDOM):
    """
    TODO
        - manipulate the CDS into a tree structure in this class? then wont dynamically update if change inputs tho
        - other options to pass, node spacing/colouring?
    """
    # __implementation__ = "static/own_js/sankey.js"
    __implementation__ = os.path.join(os.path.dirname(__file__), "sankey.js")

    source = bk_properties.Instance(bk_models.ColumnDataSource)


def make_sankey(source: bk_models.ColumnDataSource) -> bk_models.HTMLBox:
    return Sankey(source=source)
