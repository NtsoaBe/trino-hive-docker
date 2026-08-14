from trino.dbapi import connect

def run_step(context):
    
    conn = connect(
        host="localhost",
        port=8080,
        user="python",
        catalog="iceberg"
    )
    
    # table_name = context.get('target_table', 'default_table')
    # schema_name = context.get('target_schema', 'default_table')

    table_name = context.get_formatted('target_table') if 'target_table' in context else 'default_table'
    schema_name = context.get_formatted('target_schema') if 'target_schema' in context else 'default_table'

    print(f'table: {table_name}')
    print(f'schema: {schema_name}')
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT EXISTS (
                SELECT 1
                FROM iceberg.information_schema.tables
                WHERE table_schema = '{schema_name}'
                AND table_name = '{table_name}'
            ) AS table_exists
        """)
        rows = cur.fetchall()
        # print(type(rows), rows)
        schema_exists = rows[0][0] if rows else False
        if schema_exists:
            context["is_table_not_exist"]=False
        else:
            context["is_table_not_exist"]=True

        # print(context["is_table_not_exist"])
        
    finally:
        # always close resources
        cur.close()
        conn.close()
        