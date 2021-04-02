import csv

def writeCsv(data):
    with open('data.csv', newline = '  ') as csvfile:
        writer = csv.writer(csvfile, delimiter= ',')
        for row in data:
            writer.writerow(row["truck_id"]
                            + ", " +
                            row["plate"]
                            + ", " +
                            row["location"]
                            + ", " +
                            row["time_in"]
                            + ", " +
                            row["time_out"]
                            )
            
    