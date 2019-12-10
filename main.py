#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import bokeh.models as bk_models
import bokeh.plotting as bk_plotting
import bokeh.io as bk_io

import util
from sankey import Sankey


test_data = bk_models.ColumnDataSource({
    "source": ["Barry", "Frodo", "Frodo", "Barry", "Elvis", "Elvis", "Sarah", ],
    "target": ["Elvis", "Elvis", "Sarah", "Alice", "Sarah", "Alice", "Alice", ],
    "amount": [2, 2, 2, 2, 2, 2, 4],
})

doc = bk_plotting.curdoc()


sankey_out = Sankey(source=test_data)

doc.add_root(sankey_out)
doc.title = "sankey attempt"
