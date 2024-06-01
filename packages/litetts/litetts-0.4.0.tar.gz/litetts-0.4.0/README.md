# LiteTTS Package

A package to convert text into speech.

# Example Code 1
```python
import litetts
 
# init function to get an engine instance for the speech synthesis 
engine = litetts.init()
 
# say method on the engine that passing input text to be spoken
engine.say('Hello sir, how may I help you, sir.')
 
# run and wait method, it processes the voice commands. 
engine.runAndWait()
```