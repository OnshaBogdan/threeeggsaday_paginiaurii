# Installation guide

## 1. Make sure you have python 3.7.4+, pip and virtualenv installed
#### 1. In terminal, enter `python -v` / `python3 -v` / `python3.7 -v` . Use working value instead of `python` in next steps.
#### 2. Enter `python -m pip -- version` to check if you have pip installed.
#### 3. Enter `virtualenv` to check if you have virtualenv installed.

## 2. Setting up project dependencies
#### 1. Unzip the archive with the sources.
#### 2. Move into project folder `cd paginiaurii`
#### 3. Create virtual environment : `virtualenv -p python venv`
#### 6. Activate virtual environment:  `source venv/bin/activate` (`venv\Scripts\activate` on Windows)
#### 7. Install dependencies: `python -m pip install -r requirements.txt`


## 5. Run the script
#### 1. Make sure virtualenv is active (you should see `(venv)` at the beginning of the line)
#### 3. Set `search_query`, `search_location` and `output_file_format` in `config.json` file.
Allowed values for `output_file_format` are : `csv`, `json`, `xslx`, `excel` (two last are the same).
In case of both `search_query` and `search_location` are empty, the crawler will loop through ['AA', 'AB', ... , 'ZZ'] as the website doesn't allow to make empty search queries.
#### 4. Run spider: `python main.py`
- Output data will be stored in `data` folder
- Output files have a timestamp-based name.
- Log stores in `log.txt`

