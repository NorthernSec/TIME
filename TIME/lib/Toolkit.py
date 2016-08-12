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

def generate_unique_color(colors):
  while True:
    color = "#%06x"%random.randint(0, 0xFFFFFF)
    if color not in colors: return color
  
