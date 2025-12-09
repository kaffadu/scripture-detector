import asyncio
import websockets
import json
import logging
from typing import Set, Dict
from .config import Config

logger = logging.getLogger(__name__)

class ScreenProjector:
    def __init__(self, host: str = "0.0.0.0", port: int = None):
        self.host = host
        self.port = port or Config.WEBSOCKET_PORT
        self.connections: Set[websockets.WebSocketServerProtocol] = set()
        self.current_scripture: Dict = {}
        self.server = None
        
    async def start(self):
        """Start WebSocket server"""
        self.server = await websockets.serve(
            self._handler, 
            self.host, 
            self.port
        )
        logger.info(f"WebSocket server started on ws://{self.host}:{self.port}")
        
    async def stop(self):
        """Stop WebSocket server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            
    async def _handler(self, websocket, path):
        """Handle WebSocket connections"""
        self.connections.add(websocket)
        try:
            # Send current scripture if exists
            if self.current_scripture:
                await websocket.send(json.dumps(self.current_scripture))
                
            # Keep connection open
            async for message in websocket:
                pass
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.connections.remove(websocket)
            
    async def update_scripture(self, scripture_data: Dict):
        """Update and broadcast new scripture"""
        self.current_scripture = scripture_data
        
        # Broadcast to all connected clients
        if self.connections:
            message = json.dumps(scripture_data)
            await asyncio.gather(*[
                connection.send(message)
                for connection in self.connections
            ])
            
    def get_current_scripture(self) -> Dict:
        """Get current displayed scripture"""
        return self.current_scripture
