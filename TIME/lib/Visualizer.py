#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Visualizer
#   Generates reports
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

# Imports
import copy
import markdown
import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))

from flask import Flask, render_template

from TIME.lib.PluginManager import PluginManager as PM

class Visualizer():
  def generate_map(self, case):
    pass

  def generate_report(self, case):
    case = copy.deepcopy(case) # Ensure we don't modify the original object
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    plugins = sorted(PM.get_all_plugins(), key=lambda k: k['plugin'])
    plugins = [x for x in plugins if x["plugin"] in [n.plugin for n in case.nodes]]
    for node in case.nodes:
      node.info = markdown.markdown("\n".join(["# %s\n%s"%(x, node.info[x])
                                              for x in sorted(node.info.keys()) if node.info[x]]))
    custom_css = open(os.path.join(runPath, "templates/static/css/style.css")).read()
    with app.test_request_context("/"):
      return render_template('report.html', plugins=plugins, case=case, 
                                            custom_css = custom_css)
