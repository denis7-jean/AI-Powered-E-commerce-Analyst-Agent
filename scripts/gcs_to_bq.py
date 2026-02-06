from google.cloud import bigquery

# GCP config
PROJECT_ID = "shopify-mvp-2026"
DATASET_ID = "shopify_mvp"


def load_gcs_to_table(table_name: str, gcs_uri: str) -> None:
    client = bigquery.Client(project=PROJECT_ID)

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    # NOTE: If 'raw_item_properties' fails with mixed types (int/string),
    # consider setting schema_update_options=[ALLOW_FIELD_RELAXATION] or
    # explicitly defining a schema. For now we try autodetect.

    load_job = client.load_table_from_uri(gcs_uri, table_id, job_config=job_config)
    load_job.result()

    destination_table = client.get_table(table_id)
    print(f"Loaded {destination_table.num_rows} rows to {table_name}")


if __name__ == "__main__":
    # Task A: Events
    load_gcs_to_table(
        table_name="raw_events",
        gcs_uri="gs://shopify-mvp-2026-lan-na-ne1-raw/retailrocket/raw/events.csv",
    )

    # Task B: Category Tree
    load_gcs_to_table(
        table_name="raw_category_tree",
        gcs_uri="gs://shopify-mvp-2026-lan-na-ne1-raw/retailrocket/raw/category_tree.csv",
    )

    # Task C: Item Properties (wildcard)
    load_gcs_to_table(
        table_name="raw_item_properties",
        gcs_uri="gs://shopify-mvp-2026-lan-na-ne1-raw/retailrocket/raw/item_properties_part*.csv",
    )
