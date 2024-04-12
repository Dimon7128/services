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
        with conn.cursor() as cur:
            # Ensure the  single_value_table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS single_value_table (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )
            """)

            # Insert a new value or update the existing one
            cur.execute("""
                INSERT INTO single_value_table (id, name)
                VALUES (1, 'yossiBaliti')
                ON DUPLICATE KEY UPDATE name = 'yossiBaliti'
            """)
            conn.commit()
    except pymysql.MySQLError as e:
        # Log error and return
        print("MySQL Error:", e)
        return {
            "statusCode": 500,
            "body": "Failed to create or update table: " + str(e)
        }
    finally:
        # Close connection
        conn.close()

    return {
        "statusCode": 200,
        "body": "Table checked/created and value inserted/updated successfully!"
    }
