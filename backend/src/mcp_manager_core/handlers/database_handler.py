from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import dotenv_values

from typing import Dict, Any
from handlers.utils.schemas import PGItem, PGItemORM

import redis
from redis.commands.json.path import Path


################################## POSTGRESQL ###################################

class DBHandlerPG:
    def __init__(self):
        env_info = dotenv_values(".env")

        # pg_db_url = f"postgresql+psycopg2://{env_info["PG_USER"]}:{env_info["PG_PWD"]}@{env_info["PG_HOST"]}:{env_info["PG_PORT"]}/{env_info["PG_DB"]}"
        pg_db_url = f"postgresql+psycopg2://{env_info["PG_USER"]}:{env_info["PG_PWD"]}@localhost:{env_info["PG_PORT"]}/{env_info["PG_DB"]}"
        self.db_engine = create_engine(pg_db_url)

        self.db_session = self.db_session_scope(engine=self.db_engine)

    

    def db_fetch_server_list(self):
        # TODO: sqlalchemy ile db sorgusu oluşturulacak. "mcp_server_list" tablosunun bütün bilgileri alınacak. 
        pass
    

    def db_read(self):
        pass


    def db_insert(self, pg_entry: PGItem):
        with self.db_session_scope(self.db_engine) as session:
            session.execute(
                insert(PGItemORM),
                    [
                        {
                            "container_id": pg_entry.container_id, 
                            "mcp_server_name": pg_entry.mcp_server_name,
                            "mcp_server_description": pg_entry.mcp_server_description,
                            "function_args": pg_entry.function_args,
                            "function_body": pg_entry.function_body,
                        }
                    ])
            


    def db_update(self):
        pass


    def db_delete(self):
        pass
    

    @staticmethod
    def args_to_dict(args_string: str):
        """
        # TODO: Docstring oluşturulacak
        """
        if args_string == "":
            return {}
        else:
            args_list = args_string.replace(" ", "").split(",")
            args_list = [i.strip() for i in args_list]
            arg_dict = {arg.split(":")[0]: arg.split(":")[1] for arg in args_list}
            
            return arg_dict


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
    test_db = DBHandlerPG()

    test_args = "a: int, b: str, c: list"
    test_db.args_to_dict(args_string=test_args)
