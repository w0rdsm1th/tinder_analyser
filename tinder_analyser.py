#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

"""TODO
- sankey
- stacked line of right swipes vs matches vs messages sent vs app opens
# https://bokeh.pydata.org/en/0.11.0/docs/gallery/area_chart.html

- text analysis of messages
# preprocessing pipeline, making each step "toggle-able" to test improvements
replace substrings, standardise case
# metrics of of success: 
    meeting up
    replies
# topic model for all


"""
import pandas as pd
import numpy as np
import json

import bokeh
import plotly
import plotly.graph_objects as go
import plotly.express as px
import ipywidgets
import ipysankeywidget
from IPython.display import Image, SVG

# import gensim
import re
import spacy

import logging
from pprint import pprint

from conf import config


class TinderAnalyser:
    date_keywords = (
        "date",
        "meet up",
    )

    def __init__(self):
        self.file_path = r"data\data.json"
        self._log = logging.getLogger()
        self.data = self.read_data()
        self.own_num = config.own_num

    def read_data(self):
        # read data
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def print_summary_stats(self, data):
        def _recur_json_type_checker():
            # in case need to extract
            pass

        # print(data.keys())
        # dict_keys(['Photos', 'Spotify', 'Usage', 'Campaigns', 'Purchases',  ])
        # interesting
        # 'Usage',
        # 'Purchases', (overlay on the sankey when had gold)
        # 'Messages' (only sent for some reason tho)

        # uninteresting - empty or just file names
        # 'Photos',
        # 'Spotify',
        # 'Campaigns',
        # 'StudentVerifications',
        # 'User',

        # day with most swipes (left and right)


        data["Purchases"].keys()
        for _ in data["Purchases"].keys():
            print(data["Purchases"][_].keys())
        len(data["Purchases"]["subscription"])
        self.data["Purchases"]["subscription"][0]



        len(data["Messages"])
        data["Messages"][0]



        data["User"]  # total connections, age filter, create date, last active
        data["Usage"].keys()
        max(data["Usage"]["messages_received"].values())
        len(data["Usage"]["messages_received"].values())
        np.mean(list(data["Usage"]["messages_received"].values()))
        # 'app_opens', 'swipes_likes', 'swipes_passes', 'matches', 'messages_sent', 'messages_received'

        pass

    def get_subscription_date_ranges(self):
        # return list of tuples, date from and to
        out_list = []
        for each_purchase in self.data["Purchases"]["subscription"]:
            # dates are strings in ISO 8601 format "2017-03-11T01:16:53.300Z"
            create_date = each_purchase["create_date"].split("T")[0]
            expire_date = each_purchase["expire_date"].split("T")[0]
            out_list.append((create_date, expire_date))
        return out_list

    @staticmethod
    def _matches_responded(inp) -> int:
        # problem that source data only contains OWN messages,
        # so cannot definitively tell if the match responded
        return len([mtchs for mtchs in inp["Messages"] if len(mtchs["messages"]) > 2])

    def _arranged_date(self, inp) -> int:
        out_count = 0
        for match in inp["Messages"]:
            this_match_all_messages = " ".join([msg["message"].lower() for msg in match["messages"]])
            if any([kw in this_match_all_messages for kw in self.date_keywords]):
                if self.own_num in this_match_all_messages.strip():
                    out_count += 1
        return out_count

    def _got_number(self, inp) -> int:
        """
        impossible to say definitively if they sent me their number so have to perform
        approximate check for indicators
        :param inp:
        :return:
        """
        # if i sent my own number

        # if mention "number"? to step in and check

        pass

    ##########################################################################
    # visual exploration, plotting
    ##########################################################################

    def plot_message_sent_per_match_histogram(self):
        count_messages = pd.DataFrame({"count_messages": [len(match["messages"]) for match in self.data["Messages"]]})
        fig = px.histogram(count_messages)
        fig.show()

    def _sankey_numbers(self):
        # common data structure between different sankey methods (ipywidgets and plotly)
        right_swipes = sum(self.data["Usage"]["swipes_likes"].values())
        left_swipes = sum(self.data["Usage"]["swipes_passes"].values())

        matches = sum(self.data["Usage"]["matches"].values())
        no_matches = right_swipes - sum(self.data["Usage"]["matches"].values())

        i_message = len(self.data["Messages"])  # number of matches that i message (some check of index)
        i_dont_message = matches - i_message
        response = self._matches_responded(self.data)
        no_response = i_message - response

        went_on_date = self._arranged_date(self.data)

        return {"right_swipes": right_swipes,
                "left_swipes": left_swipes,
                "matches": matches,
                "no_matches": no_matches,
                "i_message": i_message,
                "i_dont_message": i_dont_message,
                "response": response,
                "no_response": no_response,
                "went_on_date": went_on_date,
                }

    def make_ipywidget_sankey(self, title_text="Tinder Activity Sankey Diagram"):

        sankey_stats = self._sankey_numbers()

        # 'app_opens', 'swipes_likes', 'swipes_passes', 'matches', 'messages_sent', 'messages_received'
        links = [
            {"source": "total swipes", "target": "left swipes", "value": sankey_stats["left_swipes"], "color": "blue"},
            {"source": "total swipes", "target": "right swipes", "value": sankey_stats["right_swipes"], "color": "blue"},

            {"source": "right swipes", "target": "no match", "value": sankey_stats["no_matches"], "color": "blue"},
            {"source": "right swipes", "target": "matches", "value": sankey_stats["matches"], "color": "blue"},

            {"source": "matches", "target": "i dont message", "value": sankey_stats["i_dont_message"], "color": "blue"},
            {"source": "matches", "target": "i message", "value": sankey_stats["i_message"], "color": "blue"},

            {"source": "i message", "target": "no response", "value": sankey_stats["no_response"], "color": "blue"},
            {"source": "i message", "target": "response", "value": sankey_stats["response"], "color": "blue"},

            {"source": "response", "target": "date", "value": sankey_stats["went_on_date"], "color": "blue"},
        ]

        order = [["total swipes"],
                 ["left swipes", "right swipes"],
                 ["no match", "matches"],
                 ["i dont message", "i message"],
                 ["no response", "response"],
                 ["date"],
                 ]

        layout = ipywidgets.Layout(width="1000", height="700")
        sankey = ipysankeywidget.SankeyWidget(links=links,
                                              order=order,
                                              linkLabelFormat=',',
                                              linkLabelMinWidth=0,
                                              layout=layout,
                                              margins=dict(top=20, bottom=0, left=30, right=60),
                                              )

        return sankey

    def make_plotly_sankey(self, title_text="Tinder Activity Sankey Diagram"):
        sankey_stats = self._sankey_numbers()

        # R to L categories: total swipes, matches, messages, no messages
        data_sankey = {
            "type": "sankey",
            "node": {
                "label": ["total swipes",
                          "left swipes", "right swipes",
                          "matches", "no matches",
                          "i messaged", "i didnt message",
                          "response", "no response",
                          # "date", "more"
                          ],
                "color": [
                    "blue",
                    "red", "green",
                    "red", "green",
                    "red", "green",
                    "red", "green",
                ],
                "pad": 0,
                "thickness": 10,
                "line": {
                    "color": "black",
                    "width": 0.5,
                },
                # "groups": [[0],
                #            [1, 2],
                #            [3, 4],
                #            [5, 6],
                #            [7, 8],
                #            ],
                "x": [0, 1],
                "y": [0, .5],
            },
            "link": {
                "arrangement": "freeform",  # perpendicular, snap
                "source": [0, 0, 2, 2, 3, 5, 5, ],
                "target": [1, 2, 3, 4, 5, 7, 8, ],
                "value": [
                    sankey_stats["left_swipes"], sankey_stats["right_swipes"],
                    sankey_stats["matches"], sankey_stats["no_matches"],
                    sankey_stats["i_message"], sankey_stats["i_dont_message"],
                    sankey_stats["response"], sankey_stats["no_response"],
                    # "label": [""],
                ],
            }
        }
        layout = dict(
            title=title_text,
            font=dict(
                size=10
            )
        )

        fig = dict(data=[data_sankey], layout=layout)
        plotly.offline.iplot(fig, validate=False)

        # fig = plt_go.Figure(data=[plt_go.Sankey(
        #     node=data_sankey,
        #     link=link)
        # ])
        # fig.update_layout(title_text=title_text, font_size=10)
        # fig.show()


    def likes_over_time(self, title_text=""):
        # todo
        # likes per app open
        # like/dislike ratio per day (add up to 100pc). sense of "optimism"

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=list(self.data["Usage"]["swipes_likes"].keys()),
                                 y=list(self.data["Usage"]["swipes_likes"].values()),
                                 name="likes",
                                 line_color='green'))

        fig.add_trace(go.Scatter(x=list(self.data["Usage"]["swipes_passes"].keys()),
                                 y=list(self.data["Usage"]["swipes_passes"].values()),
                                 name="passes",
                                 line_color='red'))

        fig.update_layout(title_text='Time Series with Rangeslider',
                          xaxis_rangeslider_visible=True)
        max_y = max(list(self.data["Usage"]["swipes_passes"].values()) + list(self.data["Usage"]["swipes_likes"].values()))

        # https://plot.ly/python/shapes/#highlighting-time-series-regions-with-rectangle-shapes
        # if got a tinder plus subscription or not during that time
        plus_dates = self.get_subscription_date_ranges()
        fig.update_layout(
            shapes=[
                # 1st highlight during Feb 4 - Feb 6
                go.layout.Shape(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="x",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="paper",
                    x0=x[0],
                    y0=0,
                    x1=x[1],
                    y1=1,
                    fillcolor="LightSalmon",
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                ) for x in plus_dates
            ]
        )
        fig.show()

    # TODO compare the right-swipe-to-match ratio when had gold vs when not
    # def


    ##########################################################################
    # message text analysis
    ##########################################################################



if __name__ == "__main__":
    analyser = TinderAnalyser()
    analyser.make_ipywidget_sankey()
    # analyser.make_plotly_sankey()
    # analyser.plot_message_sent_per_match_histogram()

