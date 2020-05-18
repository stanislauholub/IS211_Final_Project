#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request, redirect, url_for, flash

import urllib.request, json
import sqlite3

app = Flask(__name__)

id1 = 0
data1 = ""


# PART I - DATABASE SETUP AND INITIALIZATION

conn = sqlite3.connect('catalogue.db')
cur = conn.cursor()
# cur.execute('DROP TABLE IF EXISTS login')
# cur.execute('DROP TABLE IF EXISTS result')
cur.execute('CREATE TABLE IF NOT EXISTS login (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)')
cur.execute('CREATE TABLE IF NOT EXISTS result (res_id INTEGER PRIMARY KEY AUTOINCREMENT, id INT, Title VARCHAR(20), Authors VARCHAR(50), PageCount VARCHAR(20), MaturityRatings VARCHAR(20), Thumbnails VARCHAR(150), FOREIGN KEY(id) REFERENCES login(id))')
conn.close()

print('Data inserted successfully...')

# global data1, id1, id


# PART II - USER SIGNUP (MULTIUSER EXTRA CREDIT)

@app.route('/signup', methods = ['POST', 'GET'])
def signupForm():
    name = ""
    password = ""
    dt = ()
    value = ""
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if name != "" and password != "":
            query = '''INSERT INTO login (username, password) VALUES (?, ?);'''
            dt = (name, password)
            conn = sqlite3.connect('catalogue.db')
            cur = conn.cursor()
            cur.execute(query, dt)
            conn.commit()
            return redirect("/")
        else:
            value = 'Choose your new Username and Password!'
            return render_template("signup.html", value = value)
    return render_template("signup.html", value = value)


# PART III - INDEX + LOGIN PAGE

@app.route('/', methods = ['POST', 'GET'])
def index():
    global data1
    global id1
    value = ""
    data1 = ""
    name = ""
    password = ""
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        query = '''SELECT * FROM login WHERE username=? AND password=?;'''
        dt = (name, password)
        conn = sqlite3.connect('catalogue.db')
        cur = conn.cursor()
        cur.execute(query, dt)
        data = cur.fetchall()
        for i in data:
            id1 = i[0]
        cur.close()
        sql = 'SELECT * FROM result WHERE id=?'
        conn = sqlite3.connect('catalogue.db')
        cur1 = conn.cursor()
        cur1.execute(sql, str(id1))
        data1 = cur1.fetchall()
        conn.close()
        if len(data) > 0:
            return render_template('dashboard.html', data1 = data1)
        else:
            value = 'Incorrect Username or Password!'
            return render_template('login.html', value = value)
    return render_template('login.html', value = value)


# PART IV - BOOK CATALOGUE PAGE

@app.route('/loaddata', methods=['POST', 'GET'])
def load():
    global id1
    sql = 'SELECT * FROM result WHERE id=?'
    conn = sqlite3.connect('catalogue.db')
    cur1 = conn.cursor()
    cur1.execute(sql, str(id1))
    data1 = cur1.fetchall()
    conn.close()
    return render_template('dashboard.html', data1 = data1)


# PART V - ISBN BOOK SEARCH OPTION

@app.route('/isbnsearch', methods = ['POST', 'GET'])
def isbnsearch():
    global data1
    global id1
    isbnerror = ""
    dt = ()
    query = ""
    dataget = []
    ISBN = ""
    title = ""
    authors = []
    pagecount = ""
    maturityrating = ""
    thumbnails = ""
    str1 = ""
    title1 = ""
    count = 0
    totalItems = 0
    data = []
    item = ()
    if request.method == 'POST':
        ISBN = request.form['ISBN']
        title1 = title
        try:
            with urllib.request.urlopen('https://www.googleapis.com/books/v1/volumes?q=isbn:' + ISBN) as url:
                dataget = json.loads(url.read().decode())
                totalItems = len(dataget['items'])
            if totalItems > 0 and ISBN != "":
                for i in range(0, totalItems):
                    authorsstr = ""
                    dict1 = ()
                    dict2 = ()
                    dict1 = dataget['items'][i]['volumeInfo']
                    dict2 = dataget['items'][i]['volumeInfo']['imageLinks']
                    title = dict1.get('title', "null")
                    authors = dict1.get('authors', "null")
                    pagecount = dict1.get('pageCount', 0)
                    maturityrating = dict1.get('maturityRating', "null")
                    thumbnails = dict2.get('thumbnail', "#")
                    lnth = len(authors)
                    for j in range(0, lnth):
                        if j == 0:
                            authorsstr = authors[j]
                        else:
                            authorsstr = authorsstr + ", " + authors[j]
                    item = (title, authorsstr, pagecount, maturityrating, thumbnails)
                    data.append(item)
                return render_template('searchresults.html', data = data)
        except:
                isbnerror = 'No Book Found!'
                return render_template('dashboard.html', isbnerror = isbnerror, data1 = data1)
        if ISBN == "":
            isbnerror = 'Please enter ISBN!'
            return render_template('dashboard.html', isbnerror = isbnerror, data1 = data1)
    return render_template('dashboard.html', isbnerror = isbnerror, data1 = data1)


# PART VI - TITLE BOOK SEARCH OPTION (EXTRA CREDIT)

@app.route('/titlesearch', methods = ['POST', 'GET'])
def title_search():
    global data1
    global id1
    titleerror= ""
    dt = ()
    query = ""
    dataget = []
    ISBN = ""
    title = ""
    authors = []
    pagecount = ""
    maturityrating = ""
    thumbnails = ""
    str1 = ""
    title1 = ""
    count = 0
    totalItems = 0
    data = []
    item = ()
    if request.method == 'POST':
        title = request.form['title']
        title1 = title
        try:
            with urllib.request.urlopen('https://www.googleapis.com/books/v1/volumes?q=title:' + title.replace(" ", "%20")) as url:
                dataget = json.loads(url.read().decode())
                totalItems = len(dataget['items'])
            if totalItems > 0 and title != "":
                for i in range(0, totalItems):
                    authorsstr = ""
                    dict1 = ()
                    dict2 = ()
                    dict1 = dataget['items'][i]['volumeInfo']
                    dict2 = dataget['items'][i]['volumeInfo']['imageLinks']
                    title = dict1.get('title', "null")
                    authors = dict1.get('authors', "null")
                    pagecount = dict1.get('pageCount', 0)
                    maturityrating = dict1.get('maturityRating', "null")
                    thumbnails = dict2.get('thumbnail', "#")
                    lnth = len(authors)
                    for j in range(0, lnth):
                        if j == 0:
                            authorsstr = authors[j]
                        else:
                            authorsstr = authorsstr + ", " + authors[j]
                    item = (title, authorsstr, pagecount, maturityrating, thumbnails)
                    data.append(item)
                return render_template('searchresults.html', data = data)
        except:
                titleerror = "No Book Found!"
                return render_template('dashboard.html', titleerror = titleerror, data1 = data1)
        if title == "":
            titleerror = 'Please Enter Some Text!'
            return render_template('dashboard.html', titleerror = titleerror, data1 = data1)
    return render_template('dashboard.html', titleerror = titleerror, data1 = data1)


# PART VII - BOOK SAVE OPTION (INCL. THUMBNAILS EXTRA CREDIT) 

@app.route('/savedata', methods = ['GET', 'POST'])
def SaveData():
    global id
    title1 = ""
    str1 = ""
    pagecount = ""
    maturityrating = ""
    thumbnails = ""
    authors = ""
    count = 0
    id = ""
    if request.method == 'POST':
        title1 = request.form['title']
        authors = request.form['author']
        pagecount = request.form['pagecount']
        maturityrating = request.form['maturityratings']
        thumbnails = request.form['thumbnails']
        conn = sqlite3.connect('catalogue.db')
        cur3 = conn.cursor()
        query = '''INSERT INTO result(Title, Authors, PageCount, MaturityRatings, Thumbnails, id) Values(?, ?, ?, ?, ?, ?);'''
        authorstr = " "
        authorslst = list(authors)
        dt = (title1, authors, pagecount, maturityrating, thumbnails, id1)
        cur3.execute(query, dt)
        conn.commit()
        cur3.close()
        return redirect('/loaddata')


# PART VIII - CATALOGUE ITEMS DELETION

@app.route('/deletebook', methods = ['GET', 'POST'])
def delete():
    res_id = ""
    if request.method == 'POST':
        res_id = request.form['res_id']
        conn = sqlite3.connect('catalogue.db')
        cur4 = conn.cursor()
        query = 'DELETE FROM result WHERE res_id=?'
        cur4.execute(query, [res_id])
        conn.commit()
        cur4.close()
        return redirect('/loaddata')


if __name__ == '__main__':
    app.debug = True
    app.run()

