import mysql.connector
import random
import string 
from faker import Faker

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'password',
    database = 'trucks'
)

cursor = db.cursor()


location = ['EQY', 'WQY', 'CLK', 'OTH']

fake = Faker()

for i in range(20):
    # need random date in last year
    # need random duration bewteen 0 and 2 hours
    # need random license plate
    # need random location  

    letters = string.ascii_uppercase
    plate = ''.join(random.choice(letters) for jj in range(6))
    locIdx = random.randrange(0, 4, 1)

    dateIn = fake.date_time_this_decade()
    dateOut = fake.date_time_this_month()
    values = (plate, location[locIdx], dateIn, dateOut)

    sql = "INSERT INTO archive(plate, location, time_in, time_out) VALUES(%s, %s, %s, %s)"
    
    cursor.execute(sql, values)

db.commit()


