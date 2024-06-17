# import lib
from flask import Flask, render_template, request
import pymysql as pl

app = Flask(__name__, template_folder='templates')

# Global Variable : Connection Info
host = "localhost"
port = 3306
database = "luis_project"
username = "root"
password = "@kj0224kj@"

@app.route('/')
def index():
    return render_template('button.html')

@app.route('/execute_query', methods=['POST'])
def execute_query():
    query = "SELECT TRIM(gender), count(*) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)
    conn.commit()

    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('result.html', context=results)

@app.route('/Statistics_Weight_by_Gender_1990_6', methods=['POST'])
def Statistics_Weight_by_Gender_1990_6():
    query = "SELECT gender, AVG(1990_6), VARIANCE(1990_6), STDDEV(1990_6) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_1990_6.html', context=results)

@app.route('/Statistics_Weight_by_Gender_1995_6', methods=['POST'])
def Statistics_Weight_by_Gender_1995_6():
    query = "SELECT gender, AVG(1995_6), VARIANCE(1995_6), STDDEV(1995_6) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_1995_6.html', context=results)

@app.route('/Statistics_Weight_by_Gender_2000_6', methods=['POST'])
def Statistics_Weight_by_Gender_2000_6():
    query = "SELECT gender, AVG(2000_6), VARIANCE(2000_6), STDDEV(2000_6) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_2000_6.html', context=results)

@app.route('/Statistics_Weight_by_Gender_2005_6', methods=['POST'])
def Statistics_Weight_by_Gender_2005_6():
    query = "SELECT gender, AVG(2005_6), VARIANCE(2005_6), STDDEV(2005_6) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_2005_6.html', context=results)

@app.route('/Statistics_Weight_by_Gender_2010_6', methods=['POST'])
def Statistics_Weight_by_Gender_2010_6():
    query = "SELECT gender, AVG(2010_6), VARIANCE(2010_6), STDDEV(2010_6) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_2010_6.html', context=results)

@app.route('/Statistics_Weight_by_Gender_2015_6', methods=['POST'])
def Statistics_Weight_by_Gender_2015_6():
    query = "SELECT gender, AVG(2015_6), VARIANCE(2015_6), STDDEV(2015_6) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_2015_6.html', context=results)

@app.route('/Statistics_Weight_by_Gender_2019_6', methods=['POST'])
def Statistics_Weight_by_Gender_2019_6():
    query = "SELECT gender, AVG(2019_6), VARIANCE(2019_6), STDDEV(2019_6) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_2019_6.html', context=results)

#######################################################################################################################
@app.route('/Statistics_Weight_by_Gender_1990_14', methods=['POST'])
def Statistics_Weight_by_Gender_1990_14():
    query = "SELECT gender, AVG(1990_14), VARIANCE(1990_14), STDDEV(1990_14) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_1990_14.html', context=results)

@app.route('/Statistics_Weight_by_Gender_1995_14', methods=['POST'])
def Statistics_Weight_by_Gender_1995_14():
    query = "SELECT gender, AVG(1995_14), VARIANCE(1995_14), STDDEV(1995_14) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_1995_14.html', context=results)

@app.route('/Statistics_Weight_by_Gender_2000_14', methods=['POST'])
def Statistics_Weight_by_Gender_2000_14():
    query = "SELECT gender, AVG(2000_14), VARIANCE(2000_14), STDDEV(2000_14) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_2000_14.html', context=results)

@app.route('/Statistics_Weight_by_Gender_2005_14', methods=['POST'])
def Statistics_Weight_by_Gender_2005_14():
    query = "SELECT gender, AVG(2005_14), VARIANCE(2005_14), STDDEV(2005_14) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_2005_14.html', context=results)

@app.route('/Statistics_Weight_by_Gender_2010_14', methods=['POST'])
def Statistics_Weight_by_Gender_2010_14():
    query = "SELECT gender, AVG(2010_14), VARIANCE(2010_14), STDDEV(2010_14) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_2010_14.html', context=results)

@app.route('/Statistics_Weight_by_Gender_2015_14', methods=['POST'])
def Statistics_Weight_by_Gender_2015_14():
    query = "SELECT gender, AVG(2015_14), VARIANCE(2015_14), STDDEV(2015_14) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_2015_14.html', context=results)

@app.route('/Statistics_Weight_by_Gender_2019_14', methods=['POST'])
def Statistics_Weight_by_Gender_2019_14():
    query = "SELECT gender, AVG(2019_14), VARIANCE(2019_14), STDDEV(2019_14) FROM luis_project.weight GROUP BY gender;"
    print(f"request query : {query}")

    # Connection
    # DB Connection
    conn = pl.connect(host=host,
                      user=username,
                      passwd=password,
                      port=port,
                      database=database)

    cursor = conn.cursor()
    #Query 실행
    cursor.execute(query)
    #결과 가져오기
    results = cursor.fetchall()
    print(results)

    conn.commit()
    conn.close()
    # Add your code
    # Render result.html
    # Send result data of hive query
    return render_template('Statistics_Weight_by_Gender_2019_14.html', context=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


