#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Toolkit
#   Generic functions that may be re-used all over the code.
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

# Imports
import random
import types

def generate_unique_color(colors):
  while True:
    color = "#%06x"%random.randint(0, 0xFFFFFF)
    if color not in colors: return color
  
def getFunctions(classObj):
  functs = []
  for d in dir(classObj):
    if type(getattr(classObj, d)) == types.MethodType:
      functs.append(d)
  return functs

def to_dict(obj):
  result = obj
  if hasattr(obj, "__dict__"):
    result = obj.__dict__
    for key, value in result.items():
      if type(value) in [list, set]:
        result[key] = [to_dict(o) for o in value]
      if type(value) is dict:
        for k in value.keys(): value[k] = to_dict(value[k])
  return result
