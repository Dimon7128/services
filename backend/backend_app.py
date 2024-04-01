from flask import Flask, jsonify
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)
@app.route('/api/value')
def get_value():
    # Connect to RDS
    connection = pymysql.connect(host=os.environ['RDS_HOST'],
                                 user=os.environ['RDS_USER'],
                                 password=os.environ['RDS_PASSWORD'],
                                 database=os.environ['RDS_DB'],
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Execute a query
            cursor.execute("SELECT value FROM table_name")
            result = cursor.fetchone()
            # If no result, set a default value
            if not result:
                result = {'value': 'default_value'}  # Set your default value here
    finally:
        # Disconnect from RDS
        connection.close()
    # Return the result
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)

