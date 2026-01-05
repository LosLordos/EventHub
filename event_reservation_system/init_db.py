import mysql.connector
import json
import os

def init_db():
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    db_config = config['database']
    
    # Connect without database selected first to create it
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        auth_plugin='mysql_native_password'
    )
    cursor = conn.cursor()
    
    # Read Schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    # Execute commands
    # Split by semicolon but ignore delimiters if present (simple split for this file is fine)
    commands = schema_sql.split(';')
    
    print("Initializing Database...")
    for cmd in commands:
        if cmd.strip():
            try:
                cursor.execute(cmd)
            except mysql.connector.Error as err:
                print(f"Error executing command: {err}")
                print(f"Command: {cmd[:50]}...")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
