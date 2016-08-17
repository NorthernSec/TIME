#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Config reader to read the configuration file
#
# Software is free software released under the "Original BSD license"
#
# Copyright (c) 2016 	Pieter-Jan Moreels
# Copyright (c) 2016  NorthernSec

# Imports
import sys
import os
runPath = os.path.dirname(os.path.realpath(__file__))

import configparser
import urllib.parse
import urllib.request as req
from io import BytesIO
import gzip

class Configuration():
  ConfigParser = configparser.ConfigParser()
  ConfigParser.read(os.path.join(runPath, "../etc/configuration.ini"))
  default = {'http_proxy': '', 'plugin_config': './etc/plugins.txt'}

  INTEL_IP    = "intel_ip";    INTEL_DOMAIN = "intel_domain"
  INTEL_ASN   = "intel_asn";   INTEL_URL    = "intel_url"
  INTEL_EMAIL = "intel_email"; INTEL_SHA256 = "intel_sha256"
  INTEL_MD5   = "intel_md5";   INTEL_TEXT   = "intel_text"
  INTEL_USER  = "intel_user";  INTEL_PHONE  = "intel_phone"

  NODE_ORIGINAL = "Original"

  @classmethod
  def readSetting(cls, section, item, default):
    result = default
    try:
      if type(default) == bool:
        result = cls.ConfigParser.getboolean(section, item)
      elif type(default) == int:
        result = cls.ConfigParser.getint(section, item)
      else:
        result = cls.ConfigParser.get(section, item)
    except:
      pass
    return result

  @classmethod
  def toPath(cls, path):
    return path if os.path.isabs(path) else os.path.join(runPath, "..", path)

  # Http Proxy
  @classmethod
  def getProxy(cls):
    return cls.readSetting("Proxy", "http", cls.default['http_proxy'])

  @classmethod
  def getFile(cls, getfile):
    if "://" not in getfile: getfile = "http://%s"%getfile
    if cls.getProxy():
      proxy = req.ProxyHandler({'http': cls.getProxy(), 'https': cls.getProxy()})
      auth = req.HTTPBasicAuthHandler()
      opener = req.build_opener(proxy, auth, req.HTTPHandler)
      req.install_opener(opener)
    try:
      request  = req.Request(getfile)
      request.add_header("Accept-Encoding", "gzip, deflate, sdch")
      response = req.urlopen(request)
      content = response.read()
      if response.info().get('Content-Encoding') == "gzip":
        content = gzip.GzipFile(fileobj=BytesIO(content)).read()
      if type(content) == bytes:
        content = content.decode('utf-8')
      return content
    except Exception as e:
      # Log exception
      print("Error: %s on %s"%(str(e), getfile))
      return None

  # Plugins
  @classmethod
  def getPluginsettings(cls):
    return cls.toPath(cls.readSetting("Plugins", "pluginSettings", cls.default['plugin_config']))
