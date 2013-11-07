# -*- coding: utf-8 -*-
import os
import psycopg2
import psycopg2.extensions
import urlparse

# Received data as unicode
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

def get_connexion(renew=False):
    # Singleton
    if not renew and hasattr(get_connexion, "conn"): return get_connexion.conn
    result = urlparse.urlparse( os.getenv('DATABASE_URL', '') )
    # Extract field from url parsing
    username = getattr(result, "username", "postgres")
    password = getattr(result, "password", "postgres")
    hostname = getattr(result, "hostname", "localhost")
    database = getattr(result, "path")[1:]

    get_connexion.conn = psycopg2.connect(
        database = database,
        user     = username,
        password = password,
        host     = hostname
    )

    return get_connexion.conn

