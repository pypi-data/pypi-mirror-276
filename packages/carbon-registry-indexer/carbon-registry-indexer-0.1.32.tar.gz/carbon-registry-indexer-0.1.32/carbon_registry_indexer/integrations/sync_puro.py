import json
import os
import uuid
from datetime import datetime

from carbon_registry_indexer.models import enums, target
from . import utils, constants

import pandas as pd


def puro_projects_upsert(df, data_dir, table_name, project_location_file_name):
    """
    Process PURO projects data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    project_location_file_path = os.path.join(data_dir, project_location_file_name + ".csv")

    # schema
    projects_schema = target.Project.__table__.columns.keys()

    df['cmhq_project_id'] = ['Puro' + str(df['project_id'][i]) for i in range(len(df))]
    df['registry_of_origin'] = [enums.Registries.PuroEarth.value for _ in range(len(df))]
    df['current_registry'] = [enums.Registries.PuroEarth.value for _ in range(len(df))]
    df_cleaned = df.where(pd.notnull(df), None)
    utils.map_enums(table_name, df_cleaned)

    # project location
    project_locations = []
    for _, row in df_cleaned.iterrows():
        project_location = {
            'cmhq_project_id': row['cmhq_project_id'],
            'country': row['country'],
        }
        project_locations.append(project_location)

    df_project_location = pd.DataFrame(project_locations)
    df_project_location['project_location_id']= df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
        axis=1
    )

    if not df_project_location.empty:
        utils.update_csv(df_project_location,
                         project_location_file_path,
                         check_schema=False)
        print(f"Processed {len(df_project_location)} project locations. Data saved to {project_location_file_path}.")

    # project
    existing_columns = [col for col in projects_schema if col in df.columns]
    df_cleaned = df_cleaned[existing_columns]

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, 
                         target_csv_path,
                         check_schema=False)
        print(f"Processed {len(df)} projects. Data saved to {target_csv_path}.")

def puro_units_upsert(df, data_dir, table_name, projects_file_name, units_file_name):
    """
    Process PURO issuances data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    units_file_path = os.path.join(data_dir, units_file_name + ".csv")

    # schema
    issuances_schema = target.Issuance.__table__.columns.keys()
    units_schema = target.Unit.__table__.columns.keys()

    projects_sheet = pd.read_csv(projects_file_path)
    project_name_to_id = dict(zip(projects_sheet['project_name'], projects_sheet['cmhq_project_id']))

    df['cmhq_project_id'] = [project_name_to_id[project_name] for project_name in df['project_name']]
    df['issuance_id'] = df.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
        axis=1
    )

    df_cleaned = df.where(pd.notnull(df), None)
    valid_columns = [col for col in issuances_schema if col in df_cleaned.columns]

    df_cleaned = df_cleaned[valid_columns]

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, 
                         target_csv_path,
                         check_schema=False)
        print(f"Processed {len(df)} issuances. Data saved to {target_csv_path}.")

    df_cleaned_units = df.where(pd.notnull(df), None)
    df_cleaned_units['unit_status'] = [enums.UnitStatus.Retired.value for _ in range(len(df))]

    # double the df by copying retired units with status 'Issued'
    df_cleaned_units_issued = df_cleaned_units.copy()
    df_cleaned_units_issued['unit_status'] = [enums.UnitStatus.Issued.value for _ in range(len(df))]

    df_cleaned_units = pd.concat([df_cleaned_units, df_cleaned_units_issued], ignore_index=True)

    df_cleaned_units = df.where(pd.notnull(df), None)
    df_cleaned_units['cmhq_unit_id'] = df_cleaned_units.apply(
        lambda row: utils.generate_uuid_from_row(row, ['last_status_update', 'unit_count', 'unit_type', 'unit_owner', 'unit_status_reason', 'cmhq_project_id' 'unit_status']),
        axis=1
    )

    valid_columns = [col for col in units_schema if col in df_cleaned_units.columns]
    df_cleaned_units = df_cleaned_units[valid_columns]

    if not df_cleaned_units.empty:
        utils.update_csv(df_cleaned_units, 
                         units_file_path,
                         check_schema=False)
        print(f"Processed {len(df)} units. Data saved to {units_file_path}.")
    