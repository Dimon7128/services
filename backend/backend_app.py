from flask import Flask, jsonify
from flask_apscheduler import APScheduler
import pymysql
import os
import logging

class Config:
    SCHEDULER_API_ENABLED = True

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()])

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

fetched_value = None  # Global variable to store the fetched value

# Your database connection and query logic
def fetch_value():
    global fetched_value  # Declare global to modify it
    try:
        connection = pymysql.connect(host=os.environ['RDS_HOST'],
                                     user=os.environ['RDS_USER'],
                                     password=os.environ['RDS_PASSWORD'],
                                     database=os.environ['RDS_DB'],
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM single_value_table WHERE id = 1")
            result = cursor.fetchone()
            if result:
                fetched_value = result['name']  # Update the global variable
            logging.info("Fetched value: %s", result)
    except Exception as e:
        logging.error("Error fetching value: %s", e)
    finally:
        if connection:
            connection.close()

# Schedule the fetch_value function to run every 10 seconds
@scheduler.task('interval', id='fetch_value_task', seconds=10)
def scheduled_fetch_value():
    logging.info("Fetching value...")
    fetch_value()

# Define a route to return the fetched value
@app.route('/api/value')
def get_value():
    if fetched_value is not None:
        return jsonify({'value': fetched_value})
    else:
        return jsonify({'error': 'Value not fetched yet'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12345)
