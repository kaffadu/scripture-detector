import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Audio Processing
    AUDIO_SAMPLE_RATE = 16000
    AUDIO_CHUNK_DURATION = 5  # seconds
    SILENCE_THRESHOLD = 500
    VOICE_ACTIVITY_TIMEOUT = 2.0
    
    # Speech Recognition
    SPEECH_RECOGNITION_LANGUAGE = "en-US"
    GOOGLE_SPEECH_API_KEY = os.getenv("GOOGLE_SPEECH_API_KEY", "")
    
    # Bible API
    BIBLE_API_KEY = os.getenv("BIBLE_API_KEY", "")
    DEFAULT_BIBLE_VERSION = "NKJV"
    BIBLE_API_BASE_URL = "https://api.scripture.api.bible/v1"
    
    # Scripture Detection
    SCRIPTURE_PATTERN = r'(?:\d\s*)?[A-Za-z]+\s+\d+:\d+(?:-\d+)?(?:\s*[,-]?\s*\d+:\d+)*'
    BOOK_ABBREVIATIONS = {
        'gen': 'Genesis', 'exo': 'Exodus', 'lev': 'Leviticus',
        'num': 'Numbers', 'deu': 'Deuteronomy', 'jos': 'Joshua',
        'jud': 'Judges', 'rut': 'Ruth', '1sa': '1 Samuel',
        '2sa': '2 Samuel', '1ki': '1 Kings', '2ki': '2 Kings',
        '1ch': '1 Chronicles', '2ch': '2 Chronicles', 'ezr': 'Ezra',
        'neh': 'Nehemiah', 'est': 'Esther', 'job': 'Job',
        'psa': 'Psalms', 'ps': 'Psalm', 'pro': 'Proverbs',
        'ecc': 'Ecclesiastes', 'sng': 'Song of Solomon', 'isa': 'Isaiah',
        'jer': 'Jeremiah', 'lam': 'Lamentations', 'eze': 'Ezekiel',
        'dan': 'Daniel', 'hos': 'Hosea', 'jol': 'Joel',
        'amo': 'Amos', 'oba': 'Obadiah', 'jon': 'Jonah',
        'mic': 'Micah', 'nah': 'Nahum', 'hab': 'Habakkuk',
        'zep': 'Zephaniah', 'hag': 'Haggai', 'zec': 'Zechariah',
        'mal': 'Malachi', 'mat': 'Matthew', 'mrk': 'Mark',
        'luk': 'Luke', 'jhn': 'John', 'act': 'Acts',
        'rom': 'Romans', '1co': '1 Corinthians', '2co': '2 Corinthians',
        'gal': 'Galatians', 'eph': 'Ephesians', 'php': 'Philippians',
        'col': 'Colossians', '1th': '1 Thessalonians', '2th': '2 Thessalonians',
        '1ti': '1 Timothy', '2ti': '2 Timothy', 'tit': 'Titus',
        'phm': 'Philemon', 'heb': 'Hebrews', 'jas': 'James',
        '1pe': '1 Peter', '2pe': '2 Peter', '1jn': '1 John',
        '2jn': '2 John', '3jn': '3 John', 'jud': 'Jude',
        'rev': 'Revelation'
    }
    
    # WebSocket/Projection
    WEBSOCKET_PORT = 8765
    PROJECTION_UPDATE_INTERVAL = 1.0
    
    # Redis (for version preference storage)
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
