# -*- coding: utf-8 -*-
from db              import get_connexion
from ngrams          import ngrams
from psycopg2.extras import DictCursor
import argparse
import cleaner
import geo
import psycopg2
import time


NGRAM_INSERT = """INSERT INTO cable_ngram
    (cable, ngram, count, created_at)
    VALUES(%s, %s, %s, %s)
"""

LOCATION_INSERT = """INSERT INTO cable_location
    (cable, location, type, country, lat, lon, created_at)
    VALUES(%s, %s, %s, %s, %s, %s, %s)
"""

def get_cable(idx, field=None):
    conn = get_connexion()
    cur  = conn.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT * FROM cable WHERE id = %s LIMIT 1", (idx,) )
    if field == None:
        return cur.fetchone()
    else:
        return cur.fetchone().get(field)

def get_analyse(idx):
    conn  = get_connexion()
    cable = get_cable(idx=idx)
    start_time = time.time()
    # Unkown cable id
    if not cable: return "Cable %s dosen't exist!" % idx
    analyse_cable(cable, conn)
    return "cable  %s analysed (%ss)." % (idx, round(time.time() - start_time, 3))

def get_bash_analyse(frm, to, verbose=True):
    conn = get_connexion()
    cur  = conn.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT * FROM cable WHERE id >= %s AND id <= %s ORDER BY id", (frm,to) )
    cables = cur.fetchall()
    for cable in cables:
        start_time = time.time()
        analyse_cable(cable, conn)
        if verbose: print "Cable %s analysed (%ss)..." % (cable['id'], round(time.time() - start_time, 3))
    return "%s cable(s) analysed." % (len(cables),)


def analyse_cable(cable, conn):
    global NGRAM_INSERT, LOCATION_INSERT
    idx     = cable["id"]
    # Clean the data
    content = cable.get("content")
    content = cleaner.slugify(content)
    content = cleaner.stopwords(content)
    # get the ngrams
    records   = ngrams(content, n_max=3)
    cities    = geo.get_cities(content)
    countries = geo.get_cities(content)
    cur  = conn.cursor(cursor_factory=DictCursor)
    # Record ngrams, start transaction
    ngram_rows  = []
    for token, count in records.iteritems():
        row = (idx, token, count, cable['date'])
        ngram_rows.append(row)
    # Record geo location
    location_rows  = []
    # Collect city to insert
    for city in cities:
        row = (idx, city["name"].upper(), "CITY", city["countrycode"], city["latitude"], city["longitude"], cable['date'])
        location_rows.append(row)
    # Collect countries to insert
    for country in countries:
        row = (idx, country["name"], "COUNTRY", country["countrycode"], None, None, cable['date'])
        location_rows.append(row)
    try:
        cur.executemany(NGRAM_INSERT, ngram_rows)
        cur.executemany(LOCATION_INSERT, location_rows)
        conn.commit()
    except psycopg2.IntegrityError:
        # Ingnore the integrity error
        conn.rollback()
    return cable


def get_install(force=False, halt_on_error=True, table='all'):
    if table == 'all':
        install_location(force, halt_on_error)
        install_ngram(force, halt_on_error)
    elif table == 'location':
        install_location(force, halt_on_error)
    elif table == 'ngram':
        install_ngram(force, halt_on_error)

def install_location(force=False, halt_on_error=True):
    conn = get_connexion()
    cur  = conn.cursor()
    try:
        # Force new table creating by removing the existing one
        if force:
            cur.execute("""DROP TABLE cable_location""")
        cur.execute("""CREATE TABLE cable_location(
            cable      INTEGER,
            location   VARCHAR(255),
            type       VARCHAR(25),
            country    VARCHAR(25),
            lat        VARCHAR(15),
            lon        VARCHAR(15),
            created_at DATE,
            FOREIGN KEY (cable) REFERENCES cable(id),
            UNIQUE (cable, location, type)
        )""")
        # Commit actions
        conn.commit()
    except psycopg2.ProgrammingError as e:
        if halt_on_error: exit("Unable to create the table: %s" % e)
        else: pass
    print "Table ̀`cable_location` created."

def install_ngram(force=False, halt_on_error=True):
    conn = get_connexion()
    cur  = conn.cursor()
    try:
        # Force new table creating by removing the existing one
        if force:
            cur.execute("""DROP TABLE cable_ngram""")
        # Create the new tables
        cur.execute("""CREATE TABLE cable_ngram(
            cable      INTEGER,
            ngram      TEXT,
            count      INTEGER,
            created_at DATE,
            FOREIGN KEY (cable) REFERENCES cable(id),
            UNIQUE (cable, ngram)
        )""")
        # Commit actions
        conn.commit()
    except psycopg2.ProgrammingError as e:
        if halt_on_error: exit("Unable to create the table: %s" % e)
        else: pass
    print "Table ̀`cable_ngram` created."

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
    analyse = subparsers.add_parser('analyse', help="Extract ngrams from a cable.")
    # Function  that interprets this sub-command
    analyse.set_defaults(func=get_analyse)
    # Command arguments
    analyse.add_argument('idx', type=int, help="Id of the cable to analyse.")
    # ----
    # 'bash-analyse' sub-command
    # ----
    bashanalyse = subparsers.add_parser('bash-analyse', help="Extract ngrams from a range of cables.")
    # Function  that interprets this sub-command
    bashanalyse.set_defaults(func=get_bash_analyse)
    # Command arguments
    bashanalyse.add_argument('--from', dest='frm', required=True, type=int, help="Id of the first cable to analyse.")
    bashanalyse.add_argument('--to', dest='to', required=True, type=int, help="Id of the last cable to analyse.")
    # ----
    # 'install' sub-command
    # ----
    install = subparsers.add_parser('install', help="Install ngram table into the database.")
    # Command arguments
    install.add_argument('--force', dest="force", help="Force a new table creation.", action='store_true')
    install.add_argument('--no-force', dest="force", help="Do not force a new table creation.", action='store_false')
    install.add_argument('--table', dest='table', default='all', type=str, help="Table to setup (all, location, ngram).")
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