#!/usr/bin/env python3
import numpy as np
import aiy.voicehat
import aiy.audio
import numpy
import threading

# This code is run by the recorder thread
class ClapRecognizer(object):
  def __init__(self, trigger):
    self.trigger = trigger
  def add_data(self, data):
    audio = np.fromstring(data, 'int16')
    if np.max(np.abs(np.diff(audio))) > (65536 // 4):
      self.trigger.set()
 

def main():
  recorder = aiy.audio.get_recorder()
  recorder.start()  # This starts a recorder thread
  trigger = threading.Event()
  clap_recognizer = ClapRecognizer(trigger)
  recorder.add_processor(clap_recognizer)
  status_ui = aiy.voicehat.get_status_ui()
  while True:
    status_ui.status("ready")
    trigger.wait()
    status_ui.status("listening")
    try:
      aiy.audio.say("Ciao Alessandro!", lang="it-IT")
    except Exception as e:
      print("there was an error:", e)
    trigger.clear()

if __name__ == '__main__':
    main()
