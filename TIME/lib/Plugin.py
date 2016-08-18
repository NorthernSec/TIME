#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Plug-in super class
#   This class should be overridden by all plug-ins, to ensure the
#   plug-in manager is able to call the minimum required functions
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

class Plugin:
  def __init__(self, *kwargs, **args):
    pass

  def clean(self):
    pass

  def get_related_intel(self, orig_intel, intel_type):
    return []

  def get_related_info(self, orig_intel, intel_type):
    return None
