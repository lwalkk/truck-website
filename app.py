from flask import Flask, request
from flask import render_template
from flask_mysqldb import MySQL
import CreateCsv

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_DB'] = 'trucks'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])

def home():

    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM onSite''')
    data = cur.fetchall()

    return render_template('home.html', data=data)



@app.route('/archive/', methods=['POST', 'GET'])
def archive():
    cur  = mysql.connection.cursor()

    if request.method == 'POST':

        output = request.form['output']
        date= request.form['date']
        print('DATE IS  ')
        print(date)
        query = 'SELECT * FROM archive '
        andStr = ''
        whereStr = 'WHERE '

        if date !='ALL':
            if date == 'yesterday':
                query += 'WHERE time_in >= DATE_ADD(NOW(), INTERVAL -1 DAY) '
            
            elif date == 'lastWeek':
                query += 'WHERE time_in >= DATE_ADD(NOW(), INTERVAL -7 DAY) '
            
            elif date == 'last3Month':
                query += 'WHERE time_in >= DATE_ADD(NOW(), INTERVAL -90 DAY) '
            
            elif date == 'last6Month': 
                query += 'WHERE time_in >= DATE_ADD(NOW(), INTERVAL -180 DAY) ' 
            
            elif date == 'lastYear':
                query += 'WHERE time_in >= DATE_ADD(NOW(), INTERVAL -365 DAY) '

            andStr = 'AND '
            whereStr = ''

        location = request.form['location']
        
        if location != 'ALL':
            query += andStr + whereStr + 'location=' + "'"  + location + "'" + ' '
            andStr = 'AND '
            whereStr = ''
        
        #company = request.form['company']

       # if company != 'ALL':
        #    query += andStr + 'WHERE company = ' + "'" + company + "'"

        query += ';'
        print(query)

        cur.execute(query)

        data = cur.fetchall()

        displayMode = request.form['output']

        if displayMode == 'screen':
            return render_template('archive.html', data=data)


    return render_template('archive.html', data=None)



