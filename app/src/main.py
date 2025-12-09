import asyncio
import logging
import redis
import json
from typing import Optional
from .audio_processor import AudioProcessor
from .scripture_detector import ScriptureDetector
from .bible_api import BibleAPI
from .screen_projector import ScreenProjector
from .config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ScriptureProjectionApp:
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.scripture_detector = ScriptureDetector()
        self.bible_api = BibleAPI()
        self.projector = ScreenProjector()
        self.redis_client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            decode_responses=True
        )
        self.current_version = Config.DEFAULT_BIBLE_VERSION
        
    async def start(self):
        """Start the application"""
        # Start WebSocket server
        await self.projector.start()
        
        # Load saved version preference
        saved_version = self.redis_client.get("bible_version")
        if saved_version:
            self.current_version = saved_version
            logger.info(f"Loaded saved version: {self.current_version}")
        
        # Start audio processing
        self.audio_processor.start_recording(
            recognition_callback=self._on_speech_recognized,
            version_change_callback=self._on_version_change
        )
        
        logger.info("Scripture projection app started")
        logger.info(f"Current Bible version: {self.current_version}")
        
        # Keep the application running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.audio_processor.stop_recording()
            await self.projector.stop()
            
    def _on_speech_recognized(self, text: str):
        """Callback for recognized speech"""
        logger.info(f"Recognized: {text}")
        
        # Check for version change
        new_version = self.scripture_detector.detect_version_change(text)
        if new_version:
            self._handle_version_change(new_version)
            
        # Extract scripture references
        references = self.scripture_detector.extract_references(text)
        
        if references:
            logger.info(f"Found references: {references}")
            
            # Get scripture text for the first reference
            scripture = self.bible_api.get_scripture(
                references[0], 
                self.current_version
            )
            
            if scripture:
                asyncio.create_task(self._display_scripture(scripture))
                
    def _handle_version_change(self, version: str):
        """Handle Bible version change"""
        # Search for the version
        actual_version = self.bible_api.search_version(version)
        
        if actual_version:
            self.current_version = actual_version
            self.redis_client.set("bible_version", actual_version)
            logger.info(f"Bible version changed to: {actual_version}")
            
            # Display confirmation
            confirmation = {
                "reference": "Version Changed",
                "text": f"Now using {actual_version}",
                "version": actual_version,
                "type": "notification"
            }
            asyncio.create_task(self.projector.update_scripture(confirmation))
        else:
            logger.warning(f"Bible version not found: {version}")
            
    async def _display_scripture(self, scripture: dict):
        """Display scripture on screen"""
        await self.projector.update_scripture(scripture)
        logger.info(f"Displayed: {scripture['reference']}")
        
    def _on_version_change(self, version: str):
        """Handle version change from user input"""
        self._handle_version_change(version)

async def main():
    app = ScriptureProjectionApp()
    await app.start()

if __name__ == "__main__":
    asyncio.run(main())
