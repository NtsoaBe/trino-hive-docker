from trino.dbapi import connect

def run_step(context):
    
    conn = connect(
        host="localhost",
        port=8080,
        user="python",
        catalog="iceberg"
    )
    # schema_name='lake'
    schema_name = context.get('target_schema', 'default_lake')
    cur = conn.cursor()
    try:
        cur.execute(f"""SELECT schema_name
        FROM iceberg.information_schema.schemata
        WHERE schema_name = '{schema_name}'
        """)
        rows = cur.fetchall()
        if len(rows) > 0:
            context["is_schema_not_exist"]=False
        else:
            context["is_schema_not_exist"]=True
        
    finally:
        # always close resources
        cur.close()
        conn.close()
        