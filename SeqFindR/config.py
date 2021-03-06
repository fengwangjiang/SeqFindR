# Copyright 2013 Mitchell Stanton-Cook Licensed under the
#     Educational Community License, Version 2.0 (the "License"); you may
#     not use this file except in compliance with the License. You may
#     obtain a copy of the License at
#
#      http://www.osedu.org/licenses/ECL-2.0
#
#     Unless required by applicable law or agreed to in writing,
#     software distributed under the License is distributed on an "AS IS"
#     BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#     or implied. See the License for the specific language governing
#     permissions and limitations under the License.

"""
SeqFindR configuration class: 100% test coverage, >9 PyLint score
"""

import os
import sys
import ast

class SeqFindRConfig(object):
    """
    A SeqFindR configuration class - subtle manipulation to plots
    """

    def __init__(self, alt_location=None):
        self.config = read_config(alt_location)

    def __getitem__(self, key):
        try:
            return self.config[key]
        except KeyError:
            return None

    def __setitem__(self, key, item):
        # Should probably validate this ie. [(r1,g1,b1),...,(rn,gn,bn)]
        excepted = ['category_colors']
        if key in excepted:
            self.config[key] = item

    def dump_items(self):
        """
        Prints all set configuration options to STDOUT
        """
        for key, value in self.config.items():
            print ("%s = %s") % (key, value)


def read_config(alt_location):
    """
    Read a SeqFindR configuration file

    Currently only supports category colors in RGB format

    category_colors = [(0,0,0),(255,255,255),....,(r,g,b)]
    """
    if alt_location == None:
        cfg_location = os.path.expanduser('~/')+'.SeqFindR.cfg'
    else:
        cfg_location = os.path.expanduser(alt_location)
    cfg = {}
    try:
        with open(os.path.expanduser(cfg_location)) as fin:
            sys.stderr.write("Using a SeqFindR config file: %s\n" %
                                    (cfg_location))
            colors, line_count = [], 0
            for line in fin:
                line_count = line_count+1
                if line.startswith('category_colors'):
                    option, rgb_list = line.split('=')
                    option = option.strip().strip(' ')
                    rgb_list   = rgb_list.strip().strip(' ')
                    if rgb_list == '':
                        sys.stderr.write("\tNo options could be parsed. "
                                            "Using defaults\n")
                        break
                    try:
                        rgb_list = ast.literal_eval(rgb_list)
                    except (ValueError, SyntaxError) as exception:
                        sys.stderr.write("\tMalformed settings line: "
                                            "%s\n" % (str(rgb_list)))
                        break
                    for element in rgb_list:
                        try:
                            fixed = (element[0]/255.0,
                                     element[1]/255.0,
                                     element[2]/255.0)
                        except IndexError:
                            sys.stderr.write("\tMalformed RGB: %s. "
                                                "Skipping\n"
                                                % (str(element)))
                            break
                        colors.append(fixed)
                    cfg[option] = colors
                    break
                else:
                    sys.stderr.write("\tNot supported option: %s" % (line))
            if line_count == 0:
                sys.stderr.write("\tEmpty configuration file\n")
    except IOError:
        sys.stderr.write("No SeqFindR config file found at: %s. "
                            "Using defaults\n" % (cfg_location))
    return cfg
