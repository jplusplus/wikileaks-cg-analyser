# Wikileaks: Cables analyser
This project includes 4 modules to ease the document analyse: an ngrams extractor, a string cleaner, a geo references extractor and a database connector (PostGreSQL).

## Installation

**1. Prerequisite**
```bash
sudo apt-get install build-essential git-core python python-pip python-dev
sudo pip install virtualenv
```

**2.  Download the project**
```bash
git clone git@github.com:jplusplus/wikileaks-cg-analyser.git
```

**3. Install**
```bash
make install
```
## Usage
*Tokens* alway represents the string to analyse.

### String cleaner
```bash
$ python ./cleaner.py
usage: cleaner.py [-h] [-l LANGUAGE] [-c CACHE] [--slugify] [--no-slugify] tokens```
```
#### Exemple
Remove all `french` stopwords and slugify the string:
```bash
$ python ./cleaner.py -l french --slugify "Les sanglots longs des violons de l'automne blessent mon coeur d'une langueur monotone."
sanglots longs violons automne blessent coeur langueur monotone
```

### Ngrams extractor
```bash
$ python ./ngrams.py
usage: ngrams.py [-h] [-m N_MIN] [-x N_MAX] tokens
```

### Geo references extractor
```bash
$ python ./geo.py
usage: geo.py [-h] {city,country} tokens
```


## License

This software is under the [GNU GENERAL PUBLIC LICENSE v3](./LICENSE).