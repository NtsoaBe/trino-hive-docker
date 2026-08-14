import yaml
from jinja2 import Environment, FileSystemLoader
import argparse
from trino.dbapi import connect

# 1. Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--template", required=True)
parser.add_argument(
    "--layer", 
    choices=["bronze", "silver", "gold"], 
    default="bronze"  # Fallback layer if not specified
)
parser.add_argument(
    "--yaml_config", 
    default="table_weather_schema"  # Fallback schema configuration file if not specified
)
args = parser.parse_args()

template_name = args.template
target_layer = args.layer
yaml_config_file = args.yaml_config

# 2. Load the structural configuration map
with open(f"./ressource/{yaml_config_file}.yaml", "r") as f:
    spec = yaml.safe_load(f)

# 3. Dynamic Extraction: Get the dictionary configuration for the chosen layer
selected_layer_data = spec.get("layers", {}).get(target_layer, {})

# 4. Extract and inject layer-specific fields into the main template data
spec["table_name"] = selected_layer_data.get("table_name", f"weather_{target_layer}")
spec["columns"] = selected_layer_data.get("columns", [])

# 5. Clean up the dictionary payload by deleting the raw layers mapping block
if "layers" in spec:
    del spec["layers"]

# 6. Initialize Engine and Render Output Schema
env = Environment(loader=FileSystemLoader("./ressource/template_jinja"))
template = env.get_template(template_name)

sql = template.render(**spec)

# print("\nGenerated SQL:\n")
# print(sql)

# create ressource to trino now
conn = connect(
        host="localhost",
        port=8080,
        user="python",
        catalog="iceberg"
    )
cur = conn.cursor()
try:
    cur.execute(sql)
finally:
        # always close resources
        cur.close()
        conn.close()