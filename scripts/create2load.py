import re 

def process_create_tables(input_file, output_file):
    # Open the input file and read its content
    with open(input_file, 'r') as f:
        create_tables_sql = f.read()
    
    # Find all table creation statements
    table_statements = re.findall(r'CREATE TABLE\s+[\w\d_]+\s*\(.*?\);', create_tables_sql, re.DOTALL)

    # Open the output file to write the generated load statements
    with open(output_file, 'w') as out:
        for statement in table_statements:
            # Extract table name
            table_name_match = re.search(r'CREATE TABLE\s+([\w\d_]+)', statement)
            table_name = table_name_match.group(1) if table_name_match else 'unknown_table'

            # Extract column definitions
            columns = re.findall(r'(\w+)\s+(DATETIME|[^,]+)', statement)
            
            # Write the LOAD TABLE statement
            out.write(f"LOAD DATA INFILE '{table_name}.csv' INTO TABLE {table_name} FIELDS TERMINATED BY ',' LINES TERMINATED BY '\\n' IGNORE 1 LINES (\n")
            column_lines = []
            for column_name, data_type in columns:
                if 'DATETIME' in data_type.upper():
                    column_lines.append(f"    @{column_name}")
                else:
                    column_lines.append(f"    {column_name}")
            
            # Join columns with commas and ensure proper formatting
            out.write(",\n".join(column_lines) + "\n);\n")
            
            # Add conversion for DATETIME types
            for column_name, data_type in columns:
                if 'DATETIME' in data_type.upper():
                    out.write(f"SET {column_name} = STR_TO_DATE(@{column_name}, '%m/%d/%Y %H:%i');\n")

            out.write("\n-- End of load table for {}\n\n".format(table_name))

# Define input and output file paths
input_file = 'create_tables.sql'
output_file = 'load_tables.sql'

# Run the script
process_create_tables(input_file, output_file)
print(f"Load table statements have been written to {output_file}")