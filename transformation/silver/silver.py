import yaml
from pathlib import Path
from trino.dbapi import connect

def run_step(context):
    silver_config_file= context.get_formatted('silver_config_file') if 'silver_config_file' in context else 'default_silver_config_file'
    
    
    with open(silver_config_file, "r", encoding="utf-8") as f:
         config = yaml.safe_load(f)

    conn = None
    cur = None

    try:
        conn = connect(
            host=config["trino"]["host"],
            port=config["trino"]["port"],
            user=config["trino"]["user"],
            catalog=config["trino"]["catalog"],
        )
        cur = conn.cursor()
        sql = Path(config["query"]["path"]).read_text(encoding="utf-8")

        print(sql)
        cur.execute(sql)
    finally:
        print("close all connection")
        if cur is not None:
            cur.close()

        if conn is not None:
            conn.close()