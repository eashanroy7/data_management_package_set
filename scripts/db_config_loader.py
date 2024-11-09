import json

def load_db_config():
    """Load the database configuration from a JSON file."""
    with open('../config/db_config.json', 'r') as config_file:
        config = json.load(config_file)
    return config['databases']
