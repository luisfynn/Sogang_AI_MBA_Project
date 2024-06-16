import pymysql as pl
import csv

# Global variable: Connection Info
host = "localhost"
port = 3306
database = "luis_project"
username = "root"
password = "@kj0224kj@"

# Use a set to collect unique values of the first column
unique_genders = set()

def file_to_db():

    # DB connection
    conn = pl.connect(host=host, port=port, database=database, user=username, password=password)
    cursor = conn.cursor()

    # File to DB
    path = r"C:\Users\luisf\OneDrive\desktop\WorkSpace\Sogang_AI_MBA_Project\Sogang_AI_MBA_PythonProj\BigDataClouding\Project2\project2.csv"

    # with open(path, mode='r', newline='', encoding='utf-8') as f: #utf-8 사용시 mySQL에서 gender unique가 3종류가 나오는 오류 발생
    with open(path, mode = 'r', newline='', encoding= 'utf-8-sig') as f:
        csv_reader = csv.reader(f)

        for row in csv_reader:
            checkGender = row[0].strip()  # Trim any surrounding whitespace
            unique_genders.add(checkGender)

            query = "INSERT INTO weight (gender, region, 1990_6, 1990_10, 1990_14, 1990_17, 1995_6, 1995_10, 1995_14, 1995_17, 2000_6, 2000_10, 2000_14, 2000_17, 2005_6, 2005_10, 2005_14, 2005_17, 2010_6, 2010_10, 2010_14, 2010_17, 2015_6, 2015_10, 2015_14, 2015_17, 2019_6, 2019_10, 2019_14, 2019_17) "
            # query = "INSERT INTO rating (gender, region) "
            query += "VALUE ('"
            query += row[0] + "','"
            query += row[1] + "',"
            query += str(row[2]) + ","  #1990_6
            query += str(row[3]) + ","  #1990_10
            query += str(row[4]) + ","  #1990_14
            query += str(row[5]) + ","  #1990_17
            query += str(row[6]) + ","  #1995_6
            query += str(row[7]) + ","  #1995_10
            query += str(row[8]) + ","  #1995_14
            query += str(row[9]) + ","  #1995_17
            query += str(row[10]) + ","  #2000_6
            query += str(row[11]) + ","  #2000_10
            query += str(row[12]) + ","  #2000_14
            query += str(row[13]) + ","  #2000_17
            query += str(row[14]) + ","  #2005_6
            query += str(row[15]) + ","  #2005_10
            query += str(row[16]) + ","  #2005_14
            query += str(row[17]) + ","  #2005_17
            query += str(row[18]) + ","  #2010_6
            query += str(row[19]) + ","  #2010_10
            query += str(row[20]) + ","  #2010_14
            query += str(row[21]) + ","  #2010_17
            query += str(row[22]) + ","  #2015_6
            query += str(row[23]) + ","  #2015_10
            query += str(row[24]) + ","  #2015_14
            query += str(row[25]) + ","  #2015_17
            query += str(row[26]) + ","  #2019_6
            query += str(row[27]) + ","  #2019_10
            query += str(row[28]) + ","  #2019_14
            query += str(row[29]) + ")"  #2019_17

            # print(query)

            cursor.execute(query)
            conn.commit()
    conn.close()

    # Print unique values
    print("Unique genders:", unique_genders)

if __name__ == '__main__':
    file_to_db()


