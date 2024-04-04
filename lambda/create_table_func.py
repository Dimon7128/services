import pymysql
import os

def lambda_handler(event, context):
    # RDS settings
    rds_host = os.environ['RDS_HOST']
    name = os.environ['DB_USERNAME']
    password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']

    try:
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        # Log error and return
        return {
            "statusCode": 500,
            "body": str(e)
        }

    # Run query
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS table_name (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255))")
        conn.commit()

    # Close connection
    conn.close()

    return {
        "statusCode": 200,
        "body": "Query executed successfully!"
    }
