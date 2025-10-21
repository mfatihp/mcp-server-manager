from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import dotenv_values

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base


## ORM Models

Base = declarative_base()

class PGItemORM(Base):
    __tablename__ = "mcp_servers"
    id = Column(Integer, primary_key=True)
    container_id = Column(String)
    server_port = Column(String)
    mcp_server_name = Column(String)
    mcp_server_description = Column(String)
    function_args = Column(JSONB)
    function_body = Column(Text)


class DBHandlerPG:
    def __init__(self):
        env_info = dotenv_values(".env")

        pg_db_url = f"postgresql+psycopg2://{env_info["PG_USER"]}:{env_info["PG_PWD"]}@localhost:{env_info["PG_PORT"]}/{env_info["PG_DB"]}"
        self.db_engine = create_engine(pg_db_url)

        self.db_session = self.db_session_scope(engine=self.db_engine)
    

    def check_db(self):
        items = []
        # with self.db_session as session:
        with self.db_session_scope(self.db_engine) as session:
            result = session.execute(select(PGItemORM)).scalars().all()
            for item in result:
                items.append(
                    {
                        "container_id" : item.container_id,
                        "server_port" : item.server_port,
                        "mcp_server_name" : item.mcp_server_name,
                        "mcp_server_description" : item.mcp_server_description,
                        "function_args" : item.function_args
                    }
                )

        return items
    

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


if __name__ == "__main__":
    test = DBHandlerPG()
    print(test.check_db())