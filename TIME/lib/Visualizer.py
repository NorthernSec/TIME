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

from TIME.lib.Config        import Configuration as conf
from TIME.lib.PluginManager import PluginManager as PM

class Visualizer():
  @classmethod
  def generate_map(self, case):
    pass

  @classmethod
  def generate_report(self, case):
    data = self._prepare(case)
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    with app.test_request_context("/"):
      return render_template('report.html', **data)

  @classmethod
  def _prepare(self, case):
    case = copy.deepcopy(case) # Ensure we don't modify the original object
    # NOTE: For some reason, the deepcopy turns Node and Edge objects into dictionaries
    plugins = sorted(PM.get_all_plugins(), key=lambda k: k['name'])
    plugins = [x for x in plugins if x["name"] in [n['plugin'] for n in case.nodes]]
    labels = list(set([n['label'].title() for n in case.nodes]))
    if not case.notes:       case.notes = ""
    if not case.description: case.description = ""
    for node in case.nodes:
      node['label'] = node['label'].title()
      node['info'] = markdown.markdown("\n".join(["# %s\n%s"%(x, node['info'][x])
                                              for x in sorted(node['info'].keys()) if node['info'][x]]))
    intel = [x.lower() for x in dir(conf) if x.startswith("INTEL_")]
    return {'case': case, 'plugins': plugins, 'labels': labels, 'intel': intel}
