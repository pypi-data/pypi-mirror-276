from redis import Redis,ConnectionPool
import time
import uuid

class ExRedis():
    def __init__(self,redis_config):
        #self.redis = Redis(host=getConf("REDIS_HOST"),port=getConf("REDIS_PORT"),db=getConf("REDIS_DATABASE"),password=getConf("REDIS_PASSWORD"))
        self.pool = ConnectionPool.from_url(redis_config, decode_components=True) 
        self.redis = Redis(connection_pool=self.pool)
    def setValue(self,key,value,expire=3600*12):
        self.redis.set(key,value, expire)

    def getValue(self,key):
        r = self.redis.get(key)
        #self.redis.delete(key)
        if r:
            return r.decode("utf-8")
        return None

    def getValueBytes(self,key):
        r = self.redis.get(key)
        #self.redis.delete(key)
        if r:
            return r
        return None

    def getValue_wait(self,key,timeout=10):
        c=0
        while c<timeout:
            r=self.getValue(key)
            if r:
                return r
            c+=1
            time.sleep(1)

    def getValueBytes_wait(self,key,timeout=10):
        c=0
        while c<timeout:
            r=self.getValueBytes(key)
            if r:
                return r
            c+=1
            time.sleep(1)

    def push(self,key,value):
        self.redis.rpush(key,value)

    def lpush(self,key,value):
        self.redis.lpush(key,value)

    def pop_nowait(self,key):
        r=self.redis.lpop(key)
        if r:
            return r[1].decode("utf-8")
        return None

    def pop_wait(self,key):
        r=self.redis.blpop(key)
        if r:
            return r[1].decode("utf-8")
        return None

    def pop_wait_bytes(self,key):
        r=self.redis.blpop(key)
        if r:
            return r[1]
        return None

    def get_size(self,key):
        return self.redis.llen(key)

    def subscriber(self,chennal):
        ps = self.redis.pubsub()
        ps.subscribe(chennal)
        for item in ps.listen():
            if item['type'] == 'message':
                yield item['data'].decode("utf-8")
                
    def publish(self,chennal,content):
        self.redis.publish(chennal,content)

    def server_listen(self,chennal,callback):
        while True:
            item = self.pop_wait(chennal)
            callback_id=item[:32]
            content=item[32:]
            result=callback(content)
            self.setValue(chennal+"_"+callback_id,result,3600)

    def client_send(self,chennal,content,timeout=20):
        callback_id=self._get_uuid()
        callback_channel=chennal+"_"+callback_id
        _content=callback_id+content
        self.push(chennal,_content)
        r=self.getValue_wait(callback_channel,timeout)
        self.redis.delete(callback_channel)
        return r

    def client_send_bytes(self,chennal,content,timeout=20):
        callback_id=self._get_uuid()
        callback_channel=chennal+"_"+callback_id
        _content=bytes(callback_id,"utf-8")+content
        self.push(chennal,_content)
        r=self.getValueBytes_wait(callback_channel,timeout)
        self.redis.delete(callback_channel)
        return r

    def server_listen_bytes(self,chennal,callback):
        while True:
            item = self.pop_wait_bytes(chennal)
            callback_id=item[:32].decode("utf-8")
            content=item[32:]
            result=callback(content)
            self.setValue(chennal+"_"+callback_id,result,3600)

    def close(self):
        try:
            self.redis.close()
        except:
            pass

    def _get_uuid(self):
        uid = str(uuid.uuid4())
        suid = ''.join(uid.split('-'))
        return suid