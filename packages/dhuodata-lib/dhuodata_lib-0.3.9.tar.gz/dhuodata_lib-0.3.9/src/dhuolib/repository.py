from sqlalchemy import MetaData, create_engine, Table
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, scoped_session
from dhuolib.config import logger
from sqlalchemy import text


class DatabaseConnection:
    def __init__(self, username, password, host, port, service_name):
        self.engine = self._get_engine(username, password, host, port, service_name)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def _get_engine(self, username, password, host, port, service_name):
        connection_string = f"oracle+cx_oracle://{username}:{password}@{host}:{port}/?service_name={service_name}"
        self.engine = create_engine(connection_string)
        return self.engine

    @contextmanager
    def session_scope(self, expire=False):
        self.session.expire_on_commit = expire
        try:
            yield self.session
            logger.info(f"Sessão foi iniciada {self.session}")
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            logger.error(f"Erro na sessão {self.session}: {e}")
            raise
        finally:
            self.session.close()
            logger.info(f"Sessão foi finalizada {self.session}")


class GenericRepository:
    def __init__(self, data_base, table_name):
        self.db = data_base
        self.table_name = table_name
        self.metadata = MetaData()

    def load_table(self, session=None):
        return Table(self.table_name, self.metadata, autoload_with=session.bind)

    def create_table(self, list_columns: list):
        columns = [column for column in list_columns]
        schems = ", ".join(columns)
        table_schema = f"id SERIAL PRIMARY KEY, {schems}, predict_result VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        with self.db.session_scope() as session:
            query = text(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({table_schema})")
            session.execute(query)

    def insert(self, table: dict):
        with self.db.session_scope() as session:
            session.execute(
                text(
                    f"INSERT INTO {self.table_name} ({', '.join(table.keys())}) VALUES ({', '.join([f':{key}' for key in table.keys()])})"),
                table,
            )
            inserted_predict = session.execute(text(
                f"SELECT * FROM {self.table_name} WHERE id = (SELECT MAX(id) FROM {self.table_name})")).fetchone()
        return inserted_predict

    def get_items_with_pagination(self, page, page_size):
        offset = (page - 1) * page_size
        with self.db.session_scope() as session:
            query = session.query(self.table).offset(offset).limit(page_size)
            items = query.all()
        return items

    def update(self, table: dict):
        with self.db.session_scope() as session:
            update_query = text(
                f"UPDATE {self.table_name} SET predict_result = :predict_result WHERE id = :id")
            session.execute(
                update_query, {'id': table['id'], 'predict_result': table['predict_result']})
            updated_predict = session.execute(text(
                f"SELECT * FROM {self.table_name} WHERE id = (SELECT MAX(id) FROM {self.table_name})")).fetchone()
        return updated_predict
