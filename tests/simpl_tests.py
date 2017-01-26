# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 21:22:44 2017

@author: mb
"""

from nose.tools import *
import simpl

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"
