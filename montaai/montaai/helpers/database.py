import redis
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))
redis_db = int(os.environ.get("REDIS_DB", 0))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
