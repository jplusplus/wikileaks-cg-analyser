# -*- coding: utf-8 -*-
import argparse
import nltk
import re
import os
import unicodedata
# for relative paths
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
# is it a self execution?
is_self_exe = lambda: __name__ == "__main__"

def stopwords(tokens, language='english', cache=here('cache'), remove_under=4):
    # Add cache direcotry to the nltk paths
    if cache: nltk.data.path.append(cache)
    # Removes stop words
    try:
        # Get words to remove in the given language
        s = set( nltk.corpus.stopwords.words(language) )
        # Removes those words
        filtered = filter( lambda w: not w.lower() in s, tokens.split() )
        # Removes tiny words
        filtered = filter( lambda w: len(w) > remove_under, filtered)
        return " ".join(filtered)
    except LookupError:
        # Download the data if needed
        nltk.downloader.download('stopwords', download_dir=cache, quiet=True, force=True)
        return stopwords(tokens, language, cache)

def slugify(tokens):
    # Remove specialchars
    tokens = unicodedata.normalize('NFKD', unicode(tokens) )
    tokens = tokens.encode('ascii', 'ignore')
    tokens = re.sub(r'[^a-zA-Z]+', ' ', tokens).strip('-')
    tokens = re.sub(r'[-]+', ' ', tokens)
    return tokens

def main():
    parser = argparse.ArgumentParser()
    # Command arguments
    parser.add_argument('-l', '--language', help="Language to analyse.", dest="language", default='english')
    parser.add_argument('-c', '--cache', help="Cache directory (for language corpus).", default=here('cache'))
    parser.add_argument('--slugify', dest='slugify', help="Remove the specialchars and digits", action='store_true')
    parser.add_argument('--no-slugify', dest='slugify', help="Keep the specialchars and digits", action='store_false')
    parser.add_argument('tokens', help="String to filter.")
    parser.set_defaults(slugify=False)
    # Parse arguments
    args = parser.parse_args()
    # Removes specialchars and digits
    if args.slugify: args.tokens = slugify(args.tokens)
    sw_args = vars(args)
    # Removes useless arguments
    del sw_args["slugify"]
    print "".join( stopwords(**sw_args) )

if is_self_exe(): main()