import re
import logging
from typing import List, Optional, Tuple
from .config import Config

logger = logging.getLogger(__name__)

class ScriptureDetector:
    def __init__(self):
        self.pattern = re.compile(Config.SCRIPTURE_PATTERN, re.IGNORECASE)
        self.book_abbreviations = Config.BOOK_ABBREVIATIONS
        
    def extract_references(self, text: str) -> List[str]:
        """Extract scripture references from text"""
        references = []
        
        # Find all matches
        matches = self.pattern.findall(text)
        
        for match in matches:
            # Clean and validate the reference
            clean_ref = self._clean_reference(match)
            if clean_ref and self._validate_reference(clean_ref):
                references.append(clean_ref)
                
        return references
    
    def _clean_reference(self, reference: str) -> str:
        """Clean and normalize scripture reference"""
        # Remove extra spaces
        reference = re.sub(r'\s+', ' ', reference.strip())
        
        # Handle book abbreviations
        parts = reference.split()
        if len(parts) > 1:
            book_part = parts[0].lower()
            
            # Handle numbers in book names (e.g., "1 John")
            if len(parts[0]) > 1 and parts[0][0].isdigit():
                book_part = parts[0][:2].lower() + parts[1].lower()
                parts = [parts[0] + " " + parts[1]] + parts[2:]
            elif book_part in self.book_abbreviations:
                parts[0] = self.book_abbreviations[book_part]
                
        return ' '.join(parts)
    
    def _validate_reference(self, reference: str) -> bool:
        """Basic validation of scripture reference"""
        # Check if it has at least chapter and verse
        if ':' not in reference:
            return False
            
        parts = reference.split()
        if len(parts) < 2:
            return False
            
        # Check if chapter:verse pattern exists
        chapter_verse_part = parts[-1]
        if ':' not in chapter_verse_part:
            return False
            
        return True
    
    def detect_version_change(self, text: str) -> Optional[str]:
        """Detect if speaker requests a different Bible version"""
        text_lower = text.lower()
        version_keywords = ["version", "translation", "bible"]
        
        for keyword in version_keywords:
            if keyword in text_lower:
                # Look for version names
                words = text_lower.split()
                for i, word in enumerate(words):
                    if word in ["nkjv", "kjv", "niv", "esv", "nasb", "nlt", "amp", "msg"]:
                        return word.upper()
                    elif word == "version" and i > 0:
                        # Check previous word for version type
                        prev_word = words[i-1].upper()
                        if len(prev_word) <= 5:  # Likely version abbreviation
                            return prev_word
        return None
