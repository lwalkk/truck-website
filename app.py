from flask import Flask, request
from flask import render_template
from flask_mysqldb import MySQL
import TimeCalc
from datetime import datetime, timedelta

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
    cur.execute('''SELECT * FROM on_site''')
  
    onSite = cur.fetchall()

    cur.execute('SELECT time_in, time_out FROM archive WHERE time_in >= DATE_ADD(NOW(), INTERVAL -12 HOUR);')
    prevTimes = cur.fetchall()

    wait_times = TimeCalc.CalculateWaitTime(prevTimes, onSite)

    i = 0
    for row in onSite:
      wait = wait_times[i] 
      hours = (wait-datetime.now()).total_seconds() / 3600

      temp_dict = {'wait_time' :wait,'time_remaining': hours}
      row.update(temp_dict)
      i += 1

    return render_template('home.html', data=onSite, wait_times=wait_times, curr_time = datetime.now())



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



