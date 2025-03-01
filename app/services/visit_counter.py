from typing import Dict, List, Any
import asyncio
from datetime import datetime
from ..core.redis_manager import RedisManager

from ..schemas.counter import *

from app.logging import logger

class VisitCounterService():
    def __init__(self):
        """Initialize the visit counter service with Redis manager"""
        self.page_visits = dict()
        # self.redis_manager = RedisManager()
        # self.redis_manager

    async def increment_visit(self, page_id: str) -> None:
        """
        Increment visit count for a page
        
        Args:
            page_id: Unique identifier for the page
        """
        # TODO: Implement visit count increment
        if(page_id in self.page_visits.keys()): self.page_visits[page_id] += 1
        else:   self.page_visits[page_id] = 1
        # await self.redis_manager.increment(page_id)

    async def get_visit_count(self, page_id: str) -> int:
        """
        Get current visit count for a page
        
        Args:
            page_id: Unique identifier for the page
            
        Returns:
            Current visit count
        """
        # TODO: Implement getting visit count
        if(page_id in self.page_visits.keys()): return self.page_visits[page_id]
        return 0
        
        # return await self.redis_manager.get(page_id)
