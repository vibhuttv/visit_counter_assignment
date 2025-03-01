import asyncio
from datetime import datetime
import time
from typing import Dict, List, Any, Optional

from app.logging import logger
from ..core.redis_manager import RedisManager
from ..schemas.counter import VisitCount

class VisitCounterService:
    def __init__(self, cache_ttl: int = 30):
        """Initialize the visit counter service with Redis manager"""
        self.redis_manager = RedisManager()
        self.read_cache: Dict[str, tuple[int, float]] = {}
        """
        tuples are immutable, that means once created, they cannot be changed
        if you try to change, which you change in increment_visit function
        you basically create a new tuple and the pointer will start pointing to that new tuple
        so the old tuple will still exist but it will point to a different memory location
        this is called immutability
        you can check the address of the tuple using id function
        """

        self.cache_ttl = cache_ttl
        self.write_cache: Dict[str, int] = {}
        asyncio.create_task(self.flushing_task())

    async def flushing_task(self):
        while True:
            await asyncio.sleep(self.cache_ttl)
            await self._flush_to_redis()

    async def _flush_to_redis(self):
        """Periodically flush the write cache to Redis"""
        logger.info(f"Flushing visit count cache with {len(self.write_cache)} entries.")
        write_cache_copy = self.write_cache # creating a copy of the write cache
        self.write_cache = {} # clearing the write cache
        await self.redis_manager.insert_batch_to_redis(write_cache_copy)
        return

    async def increment_visit(self, page_id: str) -> None:
        """
        Increment visit count for a page
        
        Args:
            page_id: Unique identifier for the page
        """
        # TODO: Implement visit count increment
        # success = await self.redis_manager.increment(page_id)
        # if success: # also updating the in memory cache
        #     visits = await self.redis_manager.get(page_id)
        #     self.read_cache[page_id] = (visits, time.time() + self.cache_ttl)
        # return success

        self.write_cache[page_id] = self.write_cache.get(page_id, 0) + 1  # Update write cache
        if page_id in self.read_cache:    
            visits, expiry_time = self.read_cache[page_id]
            visits += self.write_cache.get(page_id, 0)  # Calculate count for read cache
        else: 
            visits = self.write_cache[page_id]
        self.read_cache[page_id] = (visits, time.time() + self.cache_ttl)  # Update read cache

        return

    async def get_visit_count(self, page_id: str) -> VisitCount:
        """
        Get current visit count for a page
        
        Args:
            page_id: Unique identifier for the page
            
        Returns:
            Current visit count
        """
        # TODO: Implement getting visit count
        response = None
        if page_id in self.read_cache:
            visits, expiry_time = self.read_cache[page_id]
            if time.time() < expiry_time: # Checking if cache is still valid
                response = VisitCount(page_id=page_id, visits=visits, served_via="in_memory")

        if response is None:
            await self._flush_to_redis()
            visits = await self.redis_manager.get(page_id)
            served_via = str(self.redis_manager.consistent_hash.get_node(page_id))
            if "redis1" in served_via:
                served_via = "redis_6370"
            elif "redis2" in served_via:
                served_via = "redis_6371"
            else:
                served_via = "redis_6372"
            self.read_cache[page_id] = (visits, time.time() + self.cache_ttl) #updating the in_memory cache to handle future reads
            response = VisitCount(page_id=page_id, visits=visits, served_via=served_via)
        return response
