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
import gzip
import urllib.parse
import urllib.request as req
from io import BytesIO
from OpenSSL import SSL

try:
  import psycopg2
except:
  print("Dependencies missing! First run the install script.")

class Configuration():
  ConfigParser = configparser.ConfigParser()
  ConfigParser.read(os.path.join(runPath, "../etc/configuration.ini"))
  default = {'http_proxy': '',      'plugin_config': './etc/plugins.txt',
             'host': "127.0.0.1",   'port': 8350,
             'debug': True,         'threads': 1,
             'ssl': False,          'sslCert': "./ssl/TIME.crt",
                                    'sslKey':  "./ssl/TIME.key",
             'authRequired': False, 'auth_load': './etc/auth.txt',
             'dbHost': 'localhost', 'dbPort': 5432,
             'db': 'nstime',        'dbPWD': 'nstime',
             'sqlite': ':memory:'}

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
    except urllib.error.HTTPError:
      return ""
    except Exception as e:
      # Log exception
      print("Error: %s on %s"%(str(e), getfile))
      return None

  # Web server
  @classmethod
  def getFlaskSettings(cls):
    data = {'host':  cls.readSetting("Flask", "host", cls.default['host']),
            'port':  cls.readSetting("Flask", "port", cls.default['port']),
            'debug': cls.readSetting("Flask", "debug", cls.default['debug']),
            'processes': cls.readSetting("Flask", "debug", cls.default['threads'])}
    # If fallback db (sqlite), use only one thread:
    if not cls.getPSQLConnection():
      data['threaded'] = False
      data['use_reloader'] = False
    # SSL wrapper
    if cls.readSetting("SSL", "ssl", cls.default['ssl']):
      try:
        context = SSL.Context(SSL.SSLv23_METHOD)
        context.use_privatekey_file( cls.readSetting("SSL", "key",  cls.default['sslKey']))
        context.use_certificate_file(cls.readSetting("SSL", "cert", cls.default['sslCert']))
        data['ssl_context'] = contect
      except Exception as e:
        print("[!] Could not read the SSL data! SSL not enabled!")
        print(" -> %s"%e)
    return data

  @classmethod
  def loginRequired(cls):
    return cls.readSetting("Auth", "required", cls.default['authRequired'])

  @classmethod
  def getAuthLoadSettings(cls):
    return cls.toPath(cls.readSetting("Auth", "settings", cls.default['auth_load']))

  # Plugins
  @classmethod
  def getPluginsettings(cls):
    return cls.toPath(cls.readSetting("Plugins", "pluginSettings", cls.default['plugin_config']))

  # Database
  @classmethod
  def getPSQLConnection(cls):
    h   = cls.readSetting("Database", "Host", cls.default['dbHost'])
    p   = cls.readSetting("Database", "Port", cls.default['dbPort'])
    d   = cls.readSetting("Database", "db",   cls.default['db'])
    pwd = cls.readSetting("Database", "password", cls.default['dbPWD'])
    try:
      conn = psycopg2.connect("host='%s' port='%s' dbname=%s user=nstime password=%s"%(h, p, d, pwd))
    except Exception as e:
      print("%s\nSome features might be unavailable"%e)
      conn = None
    return conn

  @classmethod
  def getSQLITEPath(cls):
    return cls.readSetting("Database", "fallback", cls.default['sqlite'])
