#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

"""TODO
- read file, regularise and understand shape

- sankey
- stacked line of right swipes vs matches vs messages sent vs app opens
# https://bokeh.pydata.org/en/0.11.0/docs/gallery/area_chart.html


- text analysis of messages
# metrics of of success: 
    meeting up
    replies
# topic model for all

"""
import pandas as pd
import numpy as np
import json

import bokeh
import plotly.graph_objects as plt_go
import plotly.express as px

# import gensim
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
        data["Purchases"]["subscription"][0]


        data["Purchases"]

        len(data["Messages"])
        data["Messages"][0]



        data["User"]  # total connections, age filter, create date, last active
        data["Usage"].keys()
        max(data["Usage"]["messages_received"].values())
        len(data["Usage"]["messages_received"].values())
        np.mean(list(data["Usage"]["messages_received"].values()))
        # 'app_opens', 'swipes_likes', 'swipes_passes', 'matches', 'messages_sent', 'messages_received'

        pass

    def get_subscription_date_ranges(self, data):
        # return list of tuples, date from and to
        #
        pass

    def plot_message_sent_per_match_histogram(self):
        count_messages = [len(match["messages"]) for match in self.data["Messages"]]
        fig = px.histogram(count_messages)
        fig.show()

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
                if config.own_num in this_match_all_messages.strip():
                    out_count += 1
        return out_count

    def _got_number(self, inp) -> int:
        # if

        pass

    def make_sankey(self, title_text="Sankey Diagram"):

        def _prepare_sankey_data(inp_data):
            # R to L categories: total swipes, matches, messages, no messages
            node = {"label": ["total swipes",
                              "left swipes", "right swipes",
                              "matches", "no matches",
                              "i messaged", "i didnt message",
                              "response", "no response",
                              # "date", "more"
                              ],
                    "color": [],
                    }
            right_swipes = sum(inp_data["Usage"]["swipes_likes"].values())
            left_swipes = sum(inp_data["Usage"]["swipes_passes"].values())
            # total_swipes = right_swipes + left_swipes  # not needed

            matches = sum(inp_data["Usage"]["matches"].values())
            no_matches = right_swipes - sum(inp_data["Usage"]["matches"].values())

            i_message = len(inp_data["Messages"])  # number of matches that i message (some check of index)
            i_dont_message = matches - i_message
            response = self._matches_responded(inp_data)
            no_response = i_message - response

            date = self._arranged_date(inp_data)
            # more = ...
            # = inp_data["Messages"]
            # 'app_opens', 'swipes_likes', 'swipes_passes', 'matches', 'messages_sent', 'messages_received'

            link = {
                "source": [0, 0, 2, 2, 3, 5, 5, ],
                "target": [1, 2, 3, 4, 5, 7, 8, ],
                "value": [left_swipes, right_swipes,
                          matches, no_matches,
                          i_message, i_dont_message,
                          response, no_response,
                          ],
                # "label": [""],
            }
            return node, link

        # plotly code from https://plot.ly/python/sankey-diagram/#more-complex-sankey-diagram
        sankey_node, sankey_link = _prepare_sankey_data(self.data)

        fig = plt_go.Figure(data=[plt_go.Sankey(
            node=sankey_node,
            link=sankey_link)
        ])

        fig.update_layout(title_text=title_text, font_size=10)
        fig.show()

    def likes_over_time(self, title_text=""):
        # likes per app open
        # like/dislike ratio (add up to 100pc) over time
        pass



    def preprocess_text(self, df):
        # prep text

        pass



if __name__ == "__main__":
    analyser = TinderAnalyser()
    analyser.make_sankey()
    analyser.plot_message_sent_per_match_histogram()

