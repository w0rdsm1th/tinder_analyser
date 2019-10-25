#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import pandas as pd
import bokeh.models as bk_models
import bokeh.plotting as bk_plotting
import bokeh.io as bk_io

import util
import sankey

doc = bk_plotting.curdoc()

sample_data = pd.read_csv(util.relative_file_read(__file__, ["scratch", "sankey_csv_blocks", "sankey.csv"]))
cds = bk_models.ColumnDataSource(sample_data)
out_sankey = sankey.Sankey(data_source=cds)

doc.add_root(out_sankey)
doc.title = "sankey attempt"
