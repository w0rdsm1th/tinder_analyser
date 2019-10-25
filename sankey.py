#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""


import bokeh.core.properties as bk_properties
import bokeh.models as bk_models

import util


class Sankey(bk_models.LayoutDOM):
    __implementation__ = "static/own_js/sankey.ts"

    data_source = bk_properties.Instance(bk_models.ColumnDataSource)


def make_sankey(source: bk_models.ColumnDataSource) -> bk_models.HTMLBox:
    return Sankey(data_source=source)
