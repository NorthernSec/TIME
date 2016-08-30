#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Admin creator script
#
# Creates an admin account in the database
# Only master accounts are allowed to add and remove users
# First account registered is the master account
#
# Software is free software released under the "Modified BSD license"
#
# Copyright (c) 2015 		Pieter-Jan Moreels - pieterjan.moreels@gmail.com

# Imports
from flask_login import UserMixin

from TIME.lib.Config import Configuration

# Exception
class UserNotFoundError(Exception):
    pass

# Class
class User(UserMixin):
  def __init__(self, id, auth_instance):
    if not Configuration.loginRequired():
      self.id = "TIME"
    else:
      if not auth_instance.isValidUser(id):
        raise UserNotFoundError()
      self.id = id
      self.authenticator = auth_instance

  def authenticate(self, password):
    return self.authenticator.validateUser(self.id, password)

  @classmethod
  def get(self_class, id , auth_instance):
    try:
      return self_class(id, auth_instance)
    except UserNotFoundError:
      return None
