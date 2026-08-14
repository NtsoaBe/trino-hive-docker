import requests
import yaml
import pandas as pd
import pyarrow as pa
from pyiceberg.catalog import load_catalog
    

def run_step(context):

    ingestion_config_file= context.get_formatted('ingestion_config_file') if 'ingestion_config_file' in context else 'default_ingestion_config_file'

    with open(ingestion_config_file, "r", encoding="utf-8") as f:
         config = yaml.safe_load(f)

    weather = config["weather"]
    iceberg = config["iceberg"]
    url=weather["api"]["url"]

    params = {
        "latitude": -18.8792,
        "longitude": 47.5079,
        "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # 2. Extract hourly data
    hourly = data["hourly"]


    # 3. Convert to DataFrame
    df = pd.DataFrame({
        "raw_time": hourly["time"],
        "temperature_2m": hourly["temperature_2m"],
        "relative_humidity_2m": hourly["relative_humidity_2m"],
        "wind_speed_10m": hourly["wind_speed_10m"]
    })

    
    print("DATA TO LOAD")
    print(df.head())
    df = df.astype(str)

    catalog = load_catalog(
        iceberg["catalog_name"],
        **iceberg["properties"],
    )

    # =========================================================
    # 3. LOAD TABLE
    # =========================================================
    table = catalog.load_table("project_weather.weather_hourly_bronze")

    # =========================================================
    # 4. DATA TO INSERT
    # =========================================================
    arrow_table = pa.Table.from_pandas(df, preserve_index=False)
    table.overwrite(arrow_table)