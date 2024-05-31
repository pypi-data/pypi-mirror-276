from typing import Any
__version__ = 1.2
import time
from dataclasses import dataclass
@dataclass
class CacheEntry:
    key: str
    value: str
    ttl: int
    saved: int
class NotInCache(Exception): pass
class AlreadyInCache(Exception): pass
class NotAEntry(Exception): pass
class Cache:
    def __init__(self, cache:list[CacheEntry]=[]):
        self.cache = cache
    def getElement(self, key: str, aggressive:bool=True) -> Any:
        """Fetches a entry with this key name, if aggresive is set to True then it will raise NotInCache, otherwise it will return None"""
        for entry in self.cache:
            if not isinstance(entry, CacheEntry): raise NotAEntry
            if (time.time()-entry.saved) > entry.ttl:
                self.cache.remove(entry)
                continue
            if entry.key == key:
                return entry.value
        if aggressive: raise NotInCache
        return None
    def saveElement(self, key: str, value: Any, ttl=(5*60), aggressive:bool=True, deleteifexists:bool=False) -> Any:
        if self.doesElementExist(key):
            if deleteifexists:
                self.deleteElement(key)
            if aggressive:
                raise AlreadyInCache
        self.cache.insert(0, CacheEntry(key, value, ttl, time.time()))
        return value
    def doesElementExist(self, key:str) -> None:
        found = False
        for entry in self.cache:
            if (time.time()-entry.saved) > entry.ttl:
                self.cache.remove(entry)
                continue
            if not entry.key == key:
                continue
            else:
                found = True
                break
        return found
    def deleteElement(self, key: str):
        for entry in self.cache:
            if not isinstance(entry, CacheEntry): raise NotAEntry
            if (time.time()-entry.saved) > entry.ttl:
                self.cache.remove(entry)
                continue
            if entry.key == key:
                self.cache.remove(entry)
    def deleteElementIfExists(self, key: str):
        if self.doesElementExist(key):
            self.deleteElement(key)
            return True
        return False
    def clearCache(self):
        self.cache.clear()
    def __getitem__(self, key):
        return self.getElement(key,False)
    def __repr__(self):
        return f"<Cache {repr(self.cache)}>"
    def __len__(self):
        return len(self.cache)
    def __delitem__(self, key):
        self.deleteElement(key)