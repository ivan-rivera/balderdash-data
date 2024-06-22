# Overview

This repository is intended to support the [Balderdash web app](https://github.com/ivan-rivera/balderdash-web) by extracting datasets used to generate prompt-response pairs (e.g. rare word followed by its definition).

# Structure

Each vocabulary has its own dedicated extractor set up in `extractors/`. The extracted data is stored in `data/` as JSON files.

# For Contributors

If you would like to contribute a new vocabulary, then please consider creating an issue first. Due to downstream concerns some vocabularies may not be suitable for this project, e.g. acronyms would not work because automatic bluff generation is not set up to support them in the web app (since acronym definitions follow a particular set of rules -- each word must start with the letter of the acronym).

Once you are ready to create a pull request, then fork this repository, set it up via:

```shell
pyenv install 3.11
pyenv virtualenv 3.11 balderdash-data
pyenv local balderdash-data
exec $SHELL
pip install -r requirements.txt
```

Then you would need to create a new extractor in the `extractors/` directory and it should output a JSON file in the `data/` directory. The extractor should be named after the vocabulary it is extracting, e.g. `extractors/foo.py` would output `data/foo.json`.

In some cases it may be impractical to write a scraper, in this case submitting a PR with the data in the `data/` directory is acceptable. However, please ensure that the data is in a format that can be easily consumed by the web app and that it is correct.

After merging the PR, we will be able to update the [web app config](https://github.com/ivan-rivera/balderdash-web/blob/main/src/lib/config.js#L36) to include new categories.
