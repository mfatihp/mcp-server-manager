from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import dotenv_values

import redis


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
        env_info = dotenv_values("src/mcp_manager_core/.env")
        self.redis_db_conn = redis.Redis(host=env_info["RDS_HOST"], port=env_info["RDS_PORT"], decode_responses=True)


    def db_read(self):
        """Status check function for redis."""
        pass


    def db_insert(self):
        """Insert new mcp server names and statuses into redis."""
        pass


    def db_update(self):
        """Update mcp status in redis"""
        pass


    def db_delete(self):
        """Delete mcp server data from redis"""
        pass
        
