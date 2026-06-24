import json
import pandas as pd
import logging
from sqlalchemy import create_engine


# Logging Configuration

logging.basicConfig(
    filename="etl_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Load DB Config

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


# Extract

def extract(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        logging.info("Data extraction successful")
        return data
    except Exception as e:
        logging.error(f"Error in extraction: {e}")
        raise


# Transform

def transform(data):
    try:
        df = pd.json_normalize(data)

        df.rename(columns={
            "product.id": "product_id",
            "product.name": "product_name",
            "product.category": "category",
            "product.price": "price"
        }, inplace=True)

        # Fill missing customer_id values with 'UNKNOWN'
        df["customer_id"] = df["customer_id"].fillna("UNKNOWN")

        # Fill missing discount values with 0
        df["discount"] = df["discount"].fillna(0)

        # Remove records where quantity is less than or equal to 0
        df = df[df["quantity"] > 0]

        # Convert the 'date' column to datetime format
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # Drop rows where date conversion failed
        df = df.dropna(subset=["date"])

        # Calculate total transaction amount after applying discount
        # Formula: price × quantity × (1 - discount)
        df["total_amount"] = df["price"] * df["quantity"] * (1 - df["discount"])

        logging.info("Transformation successful")
        return df

    except Exception as e:
        logging.error(f"Transformation error: {e}")
        raise


# Create DB Connection

def get_engine(config):
    try:
        connection_string = f"postgresql+psycopg2://{config['username']}:{config['password']}@" \
                            f"{config['host']}:{config['port']}/{config['database']}"

        engine = create_engine(connection_string)
        return engine

    except Exception as e:
        logging.error(f"DB connection error: {e}")
        raise



# Load (Incremental Logic)

def load(df, engine):
    try:
        conn = engine.connect()

        # Fetch existing transaction_ids from destination table
        existing_df = pd.read_sql("SELECT transaction_id FROM sales_data", conn)
        existing_ids = set(existing_df["transaction_id"])

        # Incremental filter
        new_df = df[~df["transaction_id"].isin(existing_ids)]

        # Insert data into existing table
        if not new_df.empty:
            new_df.to_sql("sales_data", engine, if_exists="append", index=False)

        logging.info(f"{len(new_df)} records inserted into sales_data table")

        conn.close()

    except Exception as e:
        logging.error(f"Load error: {e}")
        raise

def run_pipeline():
    config = load_config()

    data = extract("sales_data.json")
    df = transform(data)

    engine = get_engine(config)
    load(df, engine)

    print("ETL Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()