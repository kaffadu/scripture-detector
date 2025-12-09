import pyaudio
import wave
import numpy as np
import logging
import threading
import queue
import time
from typing import Optional, Callable
import speech_recognition as sr

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self, sample_rate: int = 16000, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.recognition_callback = None
        self.version_change_callback = None
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        
    def start_recording(self, 
                       recognition_callback: Callable[[str], None],
                       version_change_callback: Callable[[str], None] = None):
        """Start recording and processing audio"""
        self.is_recording = True
        self.recognition_callback = recognition_callback
        self.version_change_callback = version_change_callback
        
        # Start recording thread
        record_thread = threading.Thread(target=self._record_audio)
        record_thread.daemon = True
        record_thread.start()
        
        # Start processing thread
        process_thread = threading.Thread(target=self._process_audio)
        process_thread.daemon = True
        process_thread.start()
        
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
        
    def _record_audio(self):
        """Record audio from microphone"""
        p = pyaudio.PyAudio()
        
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        logger.info("Recording started...")
        
        while self.is_recording:
            try:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                self.audio_queue.put(data)
            except Exception as e:
                logger.error(f"Error recording audio: {e}")
                
        stream.stop_stream()
        stream.close()
        p.terminate()
        
    def _process_audio(self):
        """Process recorded audio for speech recognition"""
        buffer = b""
        buffer_duration = 5  # Process in 5-second chunks
        
        while self.is_recording:
            try:
                # Collect audio chunks
                while len(buffer) < self.sample_rate * 2 * buffer_duration:  # 16-bit = 2 bytes
                    if self.audio_queue.empty():
                        time.sleep(0.1)
                        continue
                    buffer += self.audio_queue.get_nowait()
                    
                # Convert to AudioData for speech recognition
                audio_data = sr.AudioData(
                    buffer,
                    sample_rate=self.sample_rate,
                    sample_width=2
                )
                
                # Reset buffer
                buffer = b""
                
                # Try speech recognition
                try:
                    text = self.recognizer.recognize_google(audio_data)
                    
                    if text and self.recognition_callback:
                        self.recognition_callback(text)
                        
                except sr.UnknownValueError:
                    logger.debug("Could not understand audio")
                except sr.RequestError as e:
                    logger.error(f"Speech recognition error: {e}")
                    
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing audio: {e}")
