import redis
from typing import Dict, List, Optional, Any
from .consistent_hash import ConsistentHash
from .config import settings

from app.logging import logger

class RedisManager:
    def __init__(self):
        """Initialize Redis connection pools and consistent hashing"""
        self.connection_pools: Dict[str, redis.ConnectionPool] = {}
        self.redis_clients: Dict[str, redis.Redis] = {}
        
        # Parse Redis nodes from comma-separated string
        redis_nodes = [node.strip() for node in settings.REDIS_NODES.split(",") if node.strip()]
        logger.info(redis_nodes)
        self.consistent_hash = ConsistentHash(redis_nodes, settings.VIRTUAL_NODES)
        
        # TODO: Initialize connection pools for each Redis node
        for node in redis_nodes:
            # 1. Create connection pools for each Redis node
            cur = redis.ConnectionPool.from_url(node)
            self.connection_pools[node] = cur
            # 2. Initialize Redis clients
            self.redis_clients[node] = redis.Redis(connection_pool = cur)

    async def get_connection(self, key: str) -> redis.Redis:
        """
        Get Redis connection for the given key using consistent hashing
        
        Args:
            key: The key to determine which Redis node to use
            
        Returns:
            Redis client for the appropriate node
        """
        # TODO: Implement getting the appropriate Redis connection
        # 1. Use consistent hashing to determine which node should handle this key
        # 2. Return the Redis client for that node
        return self.redis_clients[r'redis://redis1:6379']
        pass

    async def increment(self, key: str, amount: int = 1) -> None:
        """
        Increment a counter in Redis
        
        Args:
            key: The key to increment
            amount: Amount to increment by
            
        Returns:
            New value of the counter
        """
        # TODO: Implement incrementing a counter
        # 1. Get the appropriate Redis connection
        # 2. Increment the counter
        # 3. Handle potential failures and retries
        
        client = await self.get_connection(key)
        valid_key = client.exists(key)
        if valid_key:
            logger.info("new " + key)
            client.incrby(key, amount)
        else:
            logger.info("---- " + key)
            client.set(key, 1)

    async def get(self, key: str) -> Optional[int]:
        """
        Get value for a key from Redis
        
        Args:
            key: The key to get
            
        Returns:
            Value of the key or None if not found
        """
        # TODO: Implement getting a value
        # 1. Get the appropriate Redis connection
        # 2. Retrieve the value
        # 3. Handle potential failures and retries
        # return 69

        logger.info("Connecting to redis")
        
        for tries in range(1, 4):
            try:
                client = await self.get_connection(key)
                valid_key = client.exists(key)
                if valid_key == 0:
                    return 0
                return client.get(key)
            except Exception as e:
                if(tries < 3):
                    logger.info(f"{tries} Retrying...")
                else:
                    logger.info(f"Redis error during get: {e}")
