import hashlib
from typing import List, Dict, Any
from bisect import bisect
from app.logging import logger

class ConsistentHash:
    def __init__(self, nodes: List[str], virtual_nodes: int = 100):
        """
        Initialize the consistent hash ring
        
        Args:
            nodes: List of node identifiers (parsed from comma-separated string)
            virtual_nodes: Number of virtual nodes per physical node
        """
        
        # TODO: Initialize the hash ring with virtual nodes
        # 1. For each physical node, create virtual_nodes number of virtual nodes
        # 2. Calculate hash for each virtual node and map it to the physical node
        # 3. Store the mapping in hash_ring and maintain sorted_keys
        self.virtual_nodes = virtual_nodes
        self.hash_ring: Dict[int, str] = {}  # Mapping of hash to node
        self.sorted_keys: List[int] = []  # Sorted list of hash values
        
        for node in nodes:
            self.add_node(node)

    def _hash(self, key: str) -> int:
        """Generate a hash for a given key using SHA-256."""
        return int(hashlib.sha256(key.encode()).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        """
        Add a new node to the hash ring
        
        Args:
            node: Node identifier to add
        """
        # TODO: Implement adding a new node
        # 1. Create virtual nodes for the new physical node
        # 2. Update hash_ring and sorted_keys
        for i in range(self.virtual_nodes):
            virtual_node_key = f"{node}#{i}"
            node_hash = self._hash(virtual_node_key)
            self.hash_ring[node_hash] = node
            self.sorted_keys.append(node_hash)
        
        self.sorted_keys.sort()

    def remove_node(self, node: str) -> None:
        """
        Remove a node from the hash ring
        
        Args:
            node: Node identifier to remove
        """
        # TODO: Implement removing a node
        # 1. Remove all virtual nodes for the given physical node
        # 2. Update hash_ring and sorted_keys
        keys_to_remove = [key for key, val in self.hash_ring.items() if val == node]
        
        for key in keys_to_remove:
            del self.hash_ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key: str) -> str:
        """
        Get the node responsible for the given key
        
        Args:
            key: The key to look up
            
        Returns:
            The node responsible for the key
        """
        # TODO: Implement node lookup
        # 1. Calculate hash of the key
        # 2. Find the first node in the ring that comes after the key's hash
        # 3. If no such node exists, wrap around to the first node
        if not self.hash_ring:
            raise ValueError("No nodes in the hash ring")
        
        key_hash = self._hash(key)
        index = bisect(self.sorted_keys, key_hash)
        
        if index == len(self.sorted_keys):
            index = 0  # Wrap around to the first node
        
        return self.hash_ring[self.sorted_keys[index]]
    