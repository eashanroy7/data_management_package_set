import psycopg2

def copy_data_to_clean_db(prod_db_conn_str, clean_db_conn_str):
    """Copy data from Production DB to Clean DB based on config"""
    # Load database configuration
    db_config = load_db_config()
    
    # Find configuration for Clean_DB
    clean_db_config = next(db for db in db_config if db["name"] == "Clean_DB")
    
    # Extract batch size and filter criteria from the config
    batch_size = clean_db_config['batch_size']
    filter_criteria = clean_db_config['filter_criteria']

    # Connect to source (production) and target (clean) databases
    prod_conn = psycopg2.connect(prod_db_conn_str)
    clean_conn = psycopg2.connect(clean_db_conn_str)

    with prod_conn.cursor() as prod_cur, clean_conn.cursor() as clean_cur:
        # Apply filter_criteria logic (e.g., all_data or filtering by time range)
        if filter_criteria == "last_3_months":
            prod_cur.execute("SELECT * FROM film WHERE release_date > NOW() - INTERVAL '1 month'")
        else:
            prod_cur.execute("SELECT * FROM film")
        
        # Fetch data in batches
        while True:
            records = prod_cur.fetchmany(batch_size)
            if not records:
                break
            
            for record in records:
                clean_cur.execute("INSERT INTO film VALUES (%s, %s, ...)", record)
            clean_conn.commit()

    # Close connections
    prod_conn.close()
    clean_conn.close()
    

def copy_clean_to_env(clean_db_conn_str, env_db_conn_str, batch_size, filter_criteria):
    """Copy data from Clean DB to environment (stage, sandbox) based on config"""
    # Implement the function logic
    pass
