#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
import re

import util

def preprocess_text(self):
    # rows are matches,
    # summary stats about the conversation: number of messages, distinct words, amount of punctuation (! and emojis)
    def _clean_message_text(msg):
        # https://stackoverflow.com/a/2400577/3596968
        translate_chars = {"&apos;": "'",
                           "&lpar;": "(",
                           "&rpar;": "(",
                           "&colon": ":",
                           # "&sol;": "",  # TODO
                           "":"", }
        pattern = re.compile(r'\b(' + '|'.join(translate_chars.keys()) + r')\b')
        return pattern.sub(lambda x: translate_chars[x.group()], msg)

    pass

def assign_class(self):
    # 1 if responded, 2 if long conversation, 3 if date
    pass

if __name__ == "__main__":
    pass