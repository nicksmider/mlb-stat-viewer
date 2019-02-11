from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from tabulate import tabulate
import sqlite3


conn = sqlite3.connect('polanco.sqlite')


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def fangraphs():
    raw_html = simple_get('https://www.fangraphs.com/statss.aspx?playerid=12907&position=OF')
    html = BeautifulSoup(raw_html, 'html.parser')
    tables = list()
    for i, li in enumerate(html.findAll('table', {'class':'rgMasterTable'})):
        table = list()
        headings = list()
        for line in li.findAll('th'):
            headings.append(line.text)
        table.append(headings)

        entry = list()
        spot = 0
        for line in li.findAll('td'):
            entry.append(line.text)
            spot += 1
            if spot % len(headings) == 0:
                table.append(entry)
                entry = list()
                spot = 0
            
        tables.append(table)
    return tables

def sql_exec(conn, sql_stmt):
    try:
        c = conn.cursor()
        c.execute(sql_stmt)
    except sqlite3.Error as e:
        print(e)
        print(sql_stmt)

def main():
    tables = fangraphs()
    for table in tables[:1]:
        #new_table = tabulate(table[1:], headers=table[0])
        #print(new_table)
        sql_creat_table = 'CREATE TABLE IF NOT EXISTS regular ('
        texts =  [str(row) + ' text' for row in table[0][:2]]
        reals = [ (str(row) + ' real').replace('%', '_Perc').replace('+', '_Plus') for row in table[0][2:]]
        keys = ',\n'.join(texts)
        keys = keys + ',\n'
        keys = keys + ',\n'.join(reals)
        sql_creat_table = sql_creat_table + '\n' + keys + '\n);'

        for i, row in enumerate(table[2:]):
            table[i][1] = '"' + table[i][1] + '"'

        insert_statements = [ ', '.join(row) for row in table[2:]]
        insert_statements = [ 'INSERT INTO regular VALUES (' + statement + ');' for statement in insert_statements]
        insert_statements = [ statement.replace(u'\xa0', u'0').replace(' %', '') for statement in insert_statements]
        #print(insert_statements)
        if conn is not None:
            sql_exec(conn, sql_creat_table)
            for statement in insert_statements[:-5]:
                sql_exec(conn, statement)
            conn.commit()
        else:
            print("Error! cannot create the database connection.")



if __name__ == '__main__':
    main()