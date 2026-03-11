import redis
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    print("Connecting to Redis...")
    r.ping()
    print("Redis Connection Successful !")
except Exception as e:
    print(f"Redis Connection Failed: {e}")
