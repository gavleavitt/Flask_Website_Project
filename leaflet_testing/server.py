#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 15:16:03 2020

@author: Gavin
"""
import http.server
import socketserver

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
