from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import dotenv_values

from typing import Dict, Any

import redis
from redis.commands.json.path import Path


################################## POSTGRESQL ###################################

class DBHandlerPG:
    def __init__(self):
        env_info = dotenv_values("src/mcp_manager_core/.env")

        pg_db_url = f"postgresql+psycopg2://{env_info["PG_USER"]}:{env_info["PG_PWD"]}@{env_info["PG_HOST"]}:{env_info["PG_PORT"]}/{env_info["PG_DB"]}"
        self.db_engine = create_engine(pg_db_url) 
    

    def db_read(self):
        pass


    def db_insert(self):
        pass


    def db_update(self):
        pass


    def db_delete(self):
        pass


    @contextmanager
    def db_session_scope(self, engine):
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        session = SessionLocal()
        
        try:
            yield session
            session.commit()
        
        except Exception:
            session.rollback()
            raise
        
        finally:
            session.close()


##################################### REDIS #####################################

class DBHandlerRDS:
    """Redis database handler"""
    def __init__(self):
        # env_info = dotenv_values("src/mcp_manager_core/.env")
        # self.redis_db_conn = redis.Redis(host=env_info["RDS_HOST"], port=env_info["RDS_PORT"], decode_responses=True)
        self.redis_db_conn = redis.Redis(host="localhost", port=6379, decode_responses=True)


    def db_read(self, contId: str):
        """Status check function for redis."""
        return self.redis_db_conn.json().get(contId)


    def db_insert(self, contId: str, contInfo: Dict[str, Any]):
        """Insert new mcp server names and statuses into redis."""
        # Redis key -> "<type>:<id>"
        self.redis_db_conn.json().set(f"contId:{contId}", "$", contInfo)


    def db_update(self, contId: str):
        """Update mcp status in redis"""
        # TODO: Edit (Modify veya Update) yöntemi çalışılacak.
        # self.redis_db_conn.json().set(f"contId:{contId}", )
        pass


    def db_delete(self, contId: str):
        """Delete mcp server data from redis"""
        self.redis_db_conn.delete(contId)
        




if __name__ == "__main__":
    test_db = DBHandlerRDS()
    test_db.db_insert(contId="1", contInfo={"name":"tool_1", "description":"Some explanation"})

    print(test_db.db_read(contId="contId:1"))

    test_db.db_delete(contId="contId:1")

    print(test_db.db_read(contId="contId:1"))
