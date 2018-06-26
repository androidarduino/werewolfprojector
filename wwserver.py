#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import logic
import sys
from tornado.ioloop import IOLoop
import serial

ser = None

try:
  ser=serial.Serial("/dev/cu.usbmodem1421",9600,timeout=1)
except:
  pass

gui = None
console = None
logic = logic.Logic()

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("index.html").generate())

class WSHandler(tornado.websocket.WebSocketHandler):

  def check_origin(self, origin):
    return True

  def open(self):
    print 'connection opened...'
    self.write_message("The server says: 'Hello'. Connection was accepted.")

  def on_message(self, message):
    global gui
    global console
    global logic
    
    if (message == "GUI"):
      gui = self
      gui.write_message("GUI registered");
    
    if (message == "CONSOLE"):
      console = self
      console.write_message("Console registered.");
      
    if (not gui is None and not console is None and console == self):
      mm = logic.processCmd(message)
      gui.write_message(mm)
      print "message delivered: ", message
      updateLights(logic.light())

  def on_close(self):
    print 'connection closed...'

def on_stdin(fd, events):
  global gui
  content = fd.readline().rstrip()
#  content = unicode(content, "utf-8")
  msg = logic.processCmd(content)
  print msg
  gui.write_message(msg)
  print "message delivered: ", content
  updateLights(logic.light())

def updateLights(lights):
  print "Light status:", lights
  if ((ser is not None) and ser.isOpen()):
    ser.write(lights + "\r\n")
    print ser.readline()

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

if __name__ == "__main__":
  application.listen(9090)
  tornado.ioloop.IOLoop.instance().add_handler(sys.stdin, on_stdin, IOLoop.READ)
  tornado.ioloop.IOLoop.instance().start()
