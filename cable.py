# -*- coding: utf-8 -*-
from db              import get_connexion
from ngrams          import ngrams
from psycopg2.extras import DictCursor
import argparse
import cleaner

def get_cable(idx, field=None):
    conn = get_connexion()
    cur  = conn.cursor(cursor_factory=DictCursor)
    cur.execute("SELECT * FROM cable WHERE id = %s LIMIT 1", (idx,) )
    if field == None:
        return cur.fetchone()
    else:
        return cur.fetchone().get(field)

def get_analyse(idx):
    content = get_cable(idx=idx, field='content')
    # Clean the data
    content = cleaner.slugify(content)
    content = cleaner.stopwords(content)
    # get the ngrams
    return ngrams(content)

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
    # Parse arguments
    args = parser.parse_args()
    # Remove function from args
    func = args.func
    del args.func
    # Get the cable and print the output
    print func(**vars(args))

if __name__ == "__main__": main()