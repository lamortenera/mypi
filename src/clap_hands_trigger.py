#!/usr/bin/env python3
import numpy as np
import aiy.voicehat
import aiy.audio
import aiy.assistant.grpc
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
  player = aiy.audio.get_player()
  ciao = aiy.audio.say_audio_data("Ciao", lang="it-IT")
  non_ho_sentito = aiy.audio.say_audio_data("Non ho sentito, puoi ripetere?", lang="it-IT") 
  recorder.start()  # This starts a recorder thread
  trigger = threading.Event()
  clap_recognizer = ClapRecognizer(trigger)
  recorder.add_processor(clap_recognizer)
  status_ui = aiy.voicehat.get_status_ui()
  assistant = aiy.assistant.grpc.get_assistant()
  while True:
    status_ui.status("ready")
    print("waiting for input")
    trigger.wait()
    status_ui.status("listening")
    try:
      player.play_bytes(*ciao)
      text, audio = assistant.recognize()
      if text is not None:
        print("your question was", text)
        aiy.audio.play_audio(audio)
      else:
        player.play_bytes(*non_ho_sentito)
    except Exception as e:
      print("there was an error:", e)
    trigger.clear()

if __name__ == '__main__':
    main()
