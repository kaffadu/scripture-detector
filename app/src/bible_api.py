import requests
import json
import logging
from typing import Optional, Dict, List
from .config import Config

logger = logging.getLogger(__name__)

class BibleAPI:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or Config.BIBLE_API_KEY
        self.base_url = Config.BIBLE_API_BASE_URL
        self.headers = {
            "api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
    def get_versions(self) -> List[Dict]:
        """Get available Bible versions"""
        try:
            response = requests.get(
                f"{self.base_url}/bibles",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()["data"]
            return []
        except Exception as e:
            logger.error(f"Error fetching Bible versions: {e}")
            return []
    
    def get_scripture(self, reference: str, version: str = None) -> Optional[Dict]:
        """Get scripture text for a reference"""
        if not version:
            version = Config.DEFAULT_BIBLE_VERSION
            
        bible_id = self._get_bible_id(version)
        if not bible_id:
            logger.error(f"Bible version {version} not found")
            return None
            
        try:
            # Clean reference
            reference = reference.strip().replace(" ", "")
            
            response = requests.get(
                f"{self.base_url}/bibles/{bible_id}/passages/{reference}",
                headers=self.headers,
                params={"content-type": "text"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "reference": data["data"]["reference"],
                    "text": data["data"]["content"],
                    "version": version
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching scripture {reference}: {e}")
            return None
    
    def _get_bible_id(self, version: str) -> Optional[str]:
        """Get Bible ID from version name"""
        versions = self.get_versions()
        for v in versions:
            if version.upper() in v["name"].upper() or version.upper() in v["abbreviation"].upper():
                return v["id"]
        return None
    
    def search_version(self, query: str) -> Optional[str]:
        """Search for Bible version by name or abbreviation"""
        versions = self.get_versions()
        query = query.upper()
        
        for v in versions:
            if query in v["name"].upper() or query in v["abbreviation"].upper():
                return v["abbreviation"]
        return None
