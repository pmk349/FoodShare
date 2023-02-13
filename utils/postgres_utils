from sqlalchemy.engine import Engine



def exec_sql(E: Engine, sql_statement: str):
    with E.connect() as conn:
        return conn.execute(sql_statement)
