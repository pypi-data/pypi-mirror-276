import os

from carbon_registry_indexer.models import target
from . import utils

import pandas as pd

project_id_mapping = {}

def cadt_projects_upsert(df, data_dir, table_name):
    """
    Process CADT projects data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    
    df.columns = [utils.camel_to_snake(col) for col in df.columns]
    df.rename(columns={"warehouse_project_id": "cadt_project_id", "description": "project_description"}, inplace=True)
    
    projects_schema = target.Project.__table__.columns.keys()
    
    df_cleaned = df.where(pd.notnull(df), None)
    utils.map_enums(table_name, df_cleaned)

    df_cleaned['cmhq_project_id'] = None

    for index, row in df_cleaned.iterrows():
        _id = utils.map_registries_for_id(row['current_registry']) + row['project_id']
        if _id in df_cleaned['cmhq_project_id'] and row['origin_project_id'] != row['project_id']:
            _id = utils.map_registries_for_id(row['current_registry']) + row['origin_project_id']
        df_cleaned.at[index, 'cmhq_project_id'] = _id

    df_cleaned.drop_duplicates(subset=['cmhq_project_id'], inplace=True)
    existing_columns = [col for col in projects_schema if col in df.columns]
    # remove columns not in schema
    df = df[existing_columns]

    # drop project_tags column
    df_cleaned.drop(columns=['project_tags'], inplace=True)
    for _, row in df_cleaned.iterrows():
        project_id_mapping[row['cadt_project_id']] = row['cmhq_project_id']
    
    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path)
        print(f"Processed {len(df)} projects. Data saved to {target_csv_path}.")

def cadt_common_upsert(df, data_dir, table_name, schema):
    """
    Process CADT sheets data and save to csv. Generic function to handle multiple tables.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")

    df.columns = [utils.camel_to_snake(col) for col in df.columns]
    if "project_id" in df.columns:
        df.rename(columns={"project_id": "cadt_project_id"}, inplace=True)
    if "cobenefit" in df.columns:
        df.rename(columns={"cobenefit": "co_benefit"}, inplace=True)
        utils.map_cadt_co_benefits(df)

    new_id = f"{utils.camel_to_snake(schema)}_id"
    df.rename(columns={"id": new_id }, inplace=True)

    utils.map_enums(table_name, df)

    df['cmhq_project_id'] = None

    for index, row in df.iterrows():
        try:    
            df.loc[index, 'cmhq_project_id'] = project_id_mapping[row['cadt_project_id']]
        except KeyError:
            print(f"Project ID {row['cadt_project_id']} not found in project_id_mapping.")
            continue
            
    # drop rows with missing cmhq_project_id
    df = df[df['cmhq_project_id'].notna()]
    schema = getattr(target, schema).__table__.columns.keys()
    existing_columns = [col for col in schema if col in df.columns]
    df = df[existing_columns]

    df_cleaned = df.where(pd.notnull(df), None)

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path)
        print(f"Processed {len(df)} {table_name}. Data saved to {target_csv_path}.")
 

def cadt_units_upsert(df, data_dir, table_name, issuances_file_name, schema):
    """
    Process CADT units data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    issuances_file_path = os.path.join(data_dir, issuances_file_name + ".csv")
    df.columns = [utils.camel_to_snake(col) for col in df.columns]
    new_id = "cadt_unit_id"
    df.rename(columns={"warehouse_unit_id": new_id}, inplace=True)

    utils.map_enums(table_name, df)

    schema_columns = getattr(target, schema).__table__.columns.keys()
    existing_columns = [col for col in schema_columns if col in df.columns]
    df = df[existing_columns]

    if not os.path.exists(issuances_file_path):
        raise FileNotFoundError(f"Issuances file {issuances_file_path} not found.")
    
    issuances_df = pd.read_csv(issuances_file_path)
    df = df[df['issuance_id'].isin(issuances_df['issuance_id'])]

    # Ensure non-null values are handled correctly
    df_cleaned = df.where(pd.notnull(df), None)
    
    # Generate cmhq_unit_id using the helper function
    df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cadt_unit_id']),
        axis=1
    )
    
    # Add issued status row if all are retired
    retired_df = df_cleaned[df_cleaned['unit_status'] == 'Retired']
    issued_df = df_cleaned[df_cleaned['unit_status'] == 'Issued']

    # Create a set of issued cadt_unit_ids
    issued_cadt_unit_ids = set(issued_df['cadt_unit_id'])

    # Filter retired rows that are not issued
    additional_rows = retired_df[~retired_df['cadt_unit_id'].isin(issued_cadt_unit_ids)].copy()

    # Change the unit_status of the additional rows to 'Issued'
    additional_rows['unit_status'] = 'Issued'

    # Concatenate the original dataframe with the additional rows
    df_cleaned = pd.concat([df_cleaned, additional_rows], ignore_index=True)

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path)
        print(f"Processed {len(df)} units. Data saved to {target_csv_path}.")

def cadt_units_json_handler(all_data, data_dir, table_name, issuances_file_name, schema):
    """
    Process CADT Verra JSON data and save to csv. 
    """
    df = pd.json_normalize(all_data)
    cadt_units_upsert(df, data_dir, table_name, issuances_file_name, schema)
