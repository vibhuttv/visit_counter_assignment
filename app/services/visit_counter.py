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
        # * Key:page_id     Value: [visits, time_when_fetched]
        self.last_flushed = 0
        self.page_visits = {}
        self.buffer_write = {}
        self.redis_manager = RedisManager()

        asyncio.create_task(self.periodic_flush())
        
        
        
    async def flush_visits(self):
        logger.info("Flushing...")
        buffer_list = self.buffer_write.items()
        self.buffer_write = {}

        self.last_flushed = time.time()
        
        for cur_page, buffer_visits in buffer_list:
            await self.redis_manager.increment(cur_page, buffer_visits)
            
            
            
            
    async def periodic_flush(self):
        while True:
            await asyncio.sleep(30)
            if self.buffer_write:
                try:
                    await self.flush_visits()
                except Exception as e:
                    logger.error(f"Flush error: {e}")

        

    async def increment_visit(self, page_id: str) -> None:
        """
        Increment visit count for a page
        
        Args:
            page_id: Unique identifier for the page
        """
        # TODO: Implement visit count increment
        
        self.buffer_write[page_id] = self.buffer_write.get(page_id, 0) + 1
        
        if(page_id in self.page_visits):    self.page_visits[page_id][0] += 1
        else:   self.page_visits[page_id] = [1, 0]
        
            
                
                

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
            
            if(time_diff <= 30):  
                logger.info("Fetched from memory")
                return (self.page_visits[page_id][0], "in_memory")
            
                
        await self.flush_visits()
        logger.info("Fetched from redis")
        
        visits = await self.redis_manager.get(page_id)
        logger.info(visits)
        self.page_visits[page_id] = [int(visits), time.time()]
        return (visits, "redis")