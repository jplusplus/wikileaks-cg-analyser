# -*- coding: utf-8 -*-
from psycopg2.extras import DictCursor
from db import get_connexion
import argparse

def get_cable(conn, idx):
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT * FROM cable WHERE id = %s LIMIT 1", (idx,) )
    return cur.fetchone()

def main():
    parser = argparse.ArgumentParser()
    # Command arguments
    parser.add_argument('idx', help="Id of the cable to extract.")
    parser.add_argument('--field', dest="field", help="Field to print.", default=None)
    # Parse arguments
    args = vars( parser.parse_args() )
    conn = get_connexion()
    # Get the cable and print the output
    cable = get_cable(conn=conn, idx=args["idx"])
    if not args["field"]: print cable
    else: print cable.get(args["field"])

if __name__ == "__main__": main()