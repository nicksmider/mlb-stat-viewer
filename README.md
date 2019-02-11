# MLB Stat Viewer

My eventual goal for this project is to make a comprehensive data scrapper for Fangraphs.

I am using this as a way to practice HTML scrapping and python data manipulation.

Currenly, it will scrape Gregory Polanco's page and import his standard statistics into an SQLite database

# Set up environment

```
git clone https://github.com/nicksmider/mlb_stat_viewer.git

cd mlb_stat_viewer

python3 -m venv .

source ./bin

pip3 install -r requirements.txt
```

# Running
```
python3 main.py
```

# Check DB

A database named `polanco.sqlite` should appear in your working directory.

A nice viewer can be found here: https://sqlitebrowser.org

