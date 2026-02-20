import yaml
import os

SCHEMA_FILE = "template_schema.yml"
TABLES_FOLDER = "data_dictionaries"
OUTPUT_FILE = "schema.yml"


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def save_yaml(data, path):
    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False)


def merge_table_metadata(schema):
    """Merge description + columns into the schema entry for that table."""
    for source in schema.get("sources", []):
        for table in source.get("tables", []):
            table_name = table.get("name")
            print(table_name)

            table_meta_path = os.path.join(TABLES_FOLDER, f'{table_name.lower()}.yml')
            if not os.path.exists(table_meta_path):
                print(f"⚠️ No metadata found for table: {table_meta_path}")
                continue
            print("📥 Loading table metadata YAML files...")
            table_description, table_columns = load_table_yaml_files(table_meta_path)

            table["description"] = table_description
            table["columns"] = table_columns

    return schema


def load_table_yaml_files(file):

    table_yaml = load_yaml(file)
    table_description = table_yaml.get("models")[0].get("description")
    table_columns = table_yaml.get("models")[0].get("columns")

    return table_description, table_columns


def main():
    print("📥 Loading schema...")
    schema = load_yaml(SCHEMA_FILE)
    print(schema)

    print("🔄 Merging...")
    merged_schema = merge_table_metadata(schema)

    print(f"💾 Saving merged schema → {OUTPUT_FILE}")
    save_yaml(merged_schema, f'dbt/models/{OUTPUT_FILE}')

    print("✅ Done! Schema enriched successfully.")


if __name__ == "__main__":
    main()