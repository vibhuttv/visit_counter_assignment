from typing import Dict, List, Any
import asyncio
# from datetime import datetime
import time
from ..core.redis_manager import RedisManager

from ..schemas.counter import *

from app.logging import logger



class VisitCounterService():
    def __init__(self):
        """Initialize the visit counter service with Redis manager"""
        # * Key:page_id     Value: (visits, time_when_fetched)
        self.page_visits = dict()
        self.redis_manager = RedisManager()

    async def increment_visit(self, page_id: str) -> None:
        """
        Increment visit count for a page
        
        Args:
            page_id: Unique identifier for the page
        """
        # TODO: Implement visit count increment
        await self.redis_manager.increment(page_id)

    async def get_visit_count(self, page_id: str) -> int:
        """
        Get current visit count for a page
        
        Args:
            page_id: Unique identifier for the page
            
        Returns:
            Current visit count
        """
        # TODO: Implement getting visit count
        
        if(page_id in self.page_visits.keys()):
            time_diff = time.time() - self.page_visits[page_id][1]
            
            if(time_diff <= 5):  
                return (self.page_visits[page_id][0], "in_memory")
            
            
        visits = await self.redis_manager.get(page_id)
        self.page_visits[page_id] = (visits, time.time())
        return (visits, "redis")