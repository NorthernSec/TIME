#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Web server 
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec
# Imports
import os
import random

from flask import Flask, render_template, request, jsonify, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from TIME.lib.Authentication import AuthenticationHandler
from TIME.lib.Case           import Case
from TIME.lib.CaseManager    import CaseManager
from TIME.lib.Config         import Configuration as conf
from TIME.lib.PluginManager  import PluginManager
from TIME.lib.User           import User
from TIME.lib.Visualizer     import Visualizer

import TIME
import TIME.lib.DatabaseLayer as db
import TIME.lib.Toolkit       as TK

# variables
root = os.path.dirname(os.path.realpath(TIME.__file__))
app = Flask(__name__, static_folder  =os.path.join(root, "web/static"),
                      template_folder=os.path.join(root, "web/templates"))
app.config['SECRET_KEY'] = str(random.getrandbits(256))

auth_handler = AuthenticationHandler()
case_manager = CaseManager()

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
  return User.get(id, auth_handler)

def login_check(funct):
  def wrapper(*args, **kwargs):
    if not current_user.is_authenticated():
      if conf.loginRequired():
        return render_template('login.html')
      else:
        person = User.get("TIME", auth_handler)
        login_user(person)
    return funct(*args, **kwargs)
  return wrapper


# routes
@app.route('/')
@login_check
def index():
  return render_template('index.html')


@app.route('/_user_settings', methods=['POST'])
@login_required
def _user_settings():
  return render_template("subpages/index_user_settings.html", user=current_user.id)


@app.route('/_cases', methods=['POST'])
@login_required
def _cases():
  cases = db.get_cases_accessible_by_user(current_user.id)
  return render_template("subpages/index_cases.html", Cases=cases)


@app.route('/quick_case', methods=['GET'])
@login_required
def quick_case():
  if 'quick_case' not in session:
    session['quick_case'] = TK.to_dict(Case(title="Quick Case"))
  data = Visualizer._prepare(Case.from_dict(session['quick_case']))
  return render_template("case.html", **data)


@app.route('/_quick_case/add_intel', methods=['GET'])
@login_required
def _quick_case_add_intel():
  if 'quick_case' not in session: return jsonify({'status': 'no_existing_quick_case'})
  try:
    intel     =request.args.get('intel', type=str)
    intel_type=request.args.get('type',  type=str)
    case          = Case.from_dict(session['quick_case'])
    nodes,  edges = case.nodes[:], case.edges[:] # Take copy of lists for diff
    case_manager.add_intel(case, intel, intel_type)
    data = Visualizer._prepare(case)
    data.pop("case")
    # Get the diff in nodes & edges
    data['nodes'] = [TK.to_dict(x) for x in case.nodes if x.uid in
                      [x.uid for x in list(set(case.nodes) - set(nodes))]]
    data['edges'] = [TK.to_dict(x) for x in case.edges if (x.source, x.target) in
                      [(x.source, x.target) for x in list(set(case.edges) - set(edges))]]
    session['quick_case'] = TK.to_dict(case)
    data['status'] = 'success'
    return jsonify(data)
  except Exception as e:
    print(e)
    return jsonify({'status': 'quick_case_intel_add_error'})


@app.route('/login', methods=['POST'])
def login_check():
  # validate username and password
  username = request.form.get('username')
  password = request.form.get('password')
  person = User.get(username, auth_handler)
  try:
    if person and person.authenticate(password):
      login_user(person)
      return index()
    else:
      return render_template('login.html', status="wrong_user_pass")
  except Exception as e:
    print(e)
    return render_template('login.html', status="outdated_database")


if __name__ == '__main__':
  app.run(**conf.getFlaskSettings())
