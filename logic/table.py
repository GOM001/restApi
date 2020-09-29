#!/usr/bin/env python
# coding: utf-8
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, dialects, Table, MetaData, Column, String, Numeric, Float
from sqlalchemy.sql import text
from sqlalchemy.types import BigInteger, Integer, DATETIME
import logging
import pandas as pd
import json

# # Extraindo os dados do Postgres para um DataFrame do Pandas

class pg_table:
    ## Gera URL para acessar o banco especifico do postgresql
    postgres_db = {'drivername': 'postgres',
                'username': 'postgres',
                'password': '1234',
                'host': 'localhost',
                'port': 5432,
                'database': 'atv_seminario'}
    url = URL(**postgres_db)


    ## Configura Engine e Metadata
    engine = create_engine(url, echo=True)
    metadata = MetaData(bind=engine)


    connection = engine.connect()
    stmt = 'select * from fluxo a        join places b on a.place_id = b.place_id        join calendario c on a.calendario_id = c.calendario_id'
    result_proxy = connection.execute(stmt)
    columns = result_proxy.keys()
    results = result_proxy.fetchall()

    fluxo = pd.DataFrame(data=results, columns=columns)

