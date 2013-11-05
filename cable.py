# -*- coding: utf-8 -*-
from db              import get_connexion
from ngrams          import ngrams
from psycopg2.extras import DictCursor
import argparse
import cleaner
import psycopg2

def get_cable(idx, field=None):
    conn = get_connexion()
    cur  = conn.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT * FROM cable WHERE id = %s LIMIT 1", (idx,) )
    if field == None:
        return cur.fetchone()
    else:
        return cur.fetchone().get(field)

def get_analyse(idx):
    cable = get_cable(idx=idx)
    # Clean the data
    content = cable.get("content")
    content = cleaner.slugify(content)
    content = cleaner.stopwords(content)
    # get the ngrams
    records = ngrams(content)
    # Establish connexion
    conn = get_connexion()
    cur  = conn.cursor(cursor_factory=DictCursor)
    cur.execute("DELETE FROM cable_ngram WHERE cable = %s", (idx,) )
    # Record ngrams, start transaction
    for token, count in records.iteritems():
        values = (idx, token, count, cable['date'])
        cur.execute("""INSERT INTO cable_ngram
            (cable, ngram, count, created_at)
            VALUES(%s, %s, %s, %s)
        """, values)
    # Commit the request
    conn.commit()
    return "%s ngram(s) collected" % len(records)


def get_install(force=False, halt_on_error=True):
    conn = get_connexion()
    cur  = conn.cursor()
    try:
        # Force new table creating by removing the existing one
        if force: cur.execute("""DROP TABLE cable_ngram""")
        # Create the new table
        cur.execute("""CREATE TABLE cable_ngram(
            cable      INTEGER,
            ngram      TEXT,
            count      INTEGER,
            created_at DATE,
            FOREIGN KEY (cable) REFERENCES cable(id)
        )""")
        # Commit actions
        conn.commit()
    except psycopg2.ProgrammingError as e:
        if halt_on_error: exit("Unable to create the table: %s" % e)
        else: pass
    return "Table ̀`cable_ngram` created."

def main():
    parser     = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # ----
    # 'get' sub-command
    # ----
    getparser  = subparsers.add_parser('get', help="Get a cable.")
    # Function  that interprets this sub-command
    getparser.set_defaults(func=get_cable)
    # Command arguments
    getparser.add_argument('idx', type=int, help="Id of the cable to extract.")
    getparser.add_argument('-f', '--field', dest="field", help="Field to print.", default=None)
    # ----
    # 'analyse' sub-command
    # ----
    analyse = subparsers.add_parser('analyse', help="Extract ngram from a cable.")
    # Function  that interprets this sub-command
    analyse.set_defaults(func=get_analyse)
    # Command arguments
    analyse.add_argument('idx', type=int, help="Id of the cable to analyse.")
    # ----
    # 'install' sub-command
    # ----
    install = subparsers.add_parser('install', help="Install ngram table into the database.")
    # Command arguments
    install.add_argument('--force', dest="force", help="Force a new table creation.", action='store_true')
    install.add_argument('--no-force', dest="force", help="Do not force a new table creation.", action='store_false')
    # Function  that interprets this sub-command
    install.set_defaults(func=get_install)
    # ----
    # Parse arguments
    args = parser.parse_args()
    # Remove function from args
    func = args.func
    del args.func
    # Get the cable and print the output
    print func(**vars(args))

if __name__ == "__main__": main()