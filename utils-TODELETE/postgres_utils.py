from sqlalchemy.engine import Engine



def exec_sql(E: Engine, sql_statement: str):
    with E.begin() as conn:
        return conn.execute(sql_statement)
#         if (...):
#             conn.commit()
#         else:
#             conn.rollback()
#
# note: not sure if these ^ are needed
