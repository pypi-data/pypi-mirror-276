"""Geoflow - Utilities"""

def drop_table(
    cur,
    conn,
    node: object
):
    """
    This method will drop a table if it exists.
    """
    table = node["output_table_name"]
    schema = node["output_table_schema"]
    cur.execute(f"""DROP TABLE IF EXISTS "{schema}"."{table}";""")
    conn.commit()

def standardize_table(
    node: object
):
    """
    This method will standardize a table by adding a geometry index and gid column.
    """
    table = node["output_table_name"]
    schema = node["output_table_schema"]

    statement = f"""
    DROP INDEX IF EXISTS {table}_geom_idx;
    ALTER TABLE "{schema}"."{table}" DROP COLUMN IF EXISTS "gid";
    CREATE INDEX {table}_geom_idx ON "{schema}"."{table}" USING GIST (geom);
    ALTER TABLE "{schema}"."{table}" ADD COLUMN gid SERIAL PRIMARY KEY;
    """
    return statement

def get_table_columns(
    cur,
    table: str,
    schema: str,
    new_table_name: str=None,
    return_as_string: bool=True
) -> str:
    """
    Method to return a list of columns for a table.
    """


    sql_field_query = f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = '{table}'
    AND table_schema = '{schema}'
    AND column_name != 'geom'
    AND column_name != 'gid';
    """

    cur.execute(sql_field_query)

    db_fields = cur.fetchall()

    fields = []

    for field in db_fields:
        if new_table_name:
            column_name = field['column_name']
            fields.append(f'"{new_table_name}"."{column_name}"')
        else:
            fields.append(f'''"{table}"."{field['column_name']}"''')

    if len(fields) == 0:
        if return_as_string:
            return ""
        else:
            return []

    string_fields = ','.join(fields)

    if return_as_string:
        return f"{string_fields}"
    else:
        return fields
