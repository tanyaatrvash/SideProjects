import sqlite3 as db

def init():
    # initializing database to store features
    conn = db.connect('spent.db')
    cur = conn.cursor()
    sql = '''
    create table if not exists expenses(
        amount number,
        category string,
        message string,
        date string
    )
    '''
    cur.execute(sql)
    conn.commit() # after creating SQL query, in order to store that info permamnently, you need to commit it
    
def log(amount, category, message=''):
    from datetime import datetime 
    date = str(datetime.now)
    
    conn = db.connect('spent.db')
    cur = conn.cursor()
    sql = '''
    insert into expenses values (
        {},
        '{}',
        '{}',
        '{}',
    )
    '''.format(amount, category, message, date)
    cur.execute(sql)
    conn.commit()

def view(category = None):
    # return list of all expenses incurred & total expense
    # if category is specified, it only returns info from that category
    conn = db.connect('spent.db')
    cur = conn.cursor()
    if category:
        sql = '''
        select * from expenses where category = '{}'
        '''.format(category)
        sql2 = '''
        select sum(amount) from expenses where category = '{}'
        '''.format(category)
    else:
        sql = '''
        select * from expenses
        '''.format(category)
        sql2 = '''
        select sum(amount) from expenses
        '''.format(category)

    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]

    return total_amount, results

print(view('food'))
print()