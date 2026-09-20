from time import time
class RateLimiter:
    def __init__(self,max_requests=30,window_seconds=60): self.max_requests=max_requests; self.window_seconds=window_seconds; self.buckets={}
    def allow(self,key):
        now=time(); bucket=[t for t in self.buckets.get(key,[]) if now-t<self.window_seconds]
        if len(bucket)>=self.max_requests: self.buckets[key]=bucket; return False
        bucket.append(now); self.buckets[key]=bucket; return True
