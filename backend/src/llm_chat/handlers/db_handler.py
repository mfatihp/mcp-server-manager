from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from dotenv import dotenv_values





class DBHandlerPG:
    def __init__(self):
        env_info = dotenv_values("db.env")

        pg_db_url = f"postgresql+psycopg2://{env_info["PG_USER"]}:{env_info["PG_PWD"]}@localhost:{env_info["PG_PORT"]}/{env_info["PG_DB"]}"
        self.db_engine = create_engine(pg_db_url)

        self.db_session = self.db_session_scope(engine=self.db_engine)
    

    def check_db(self):
        with self.db_session as session:
            session.execute(select(""))
    

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