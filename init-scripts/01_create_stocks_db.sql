\connect postgres
\set ON_ERROR_STOP on

SELECT 'CREATE DATABASE stocks' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'stocks');
\gexec

\connect stocks

CREATE TABLE IF NOT EXISTS stock_prices (
symbol TEXT    NOT NULL,
date   DATE    NOT NULL,
open   FLOAT   DEFAULT NULL,
high   FLOAT   DEFAULT NULL,
low    FLOAT   DEFAULT NULL,
close  FLOAT   DEFAULT NULL,
volume BIGINT  DEFAULT NULL,
PRIMARY KEY (symbol, date)
);