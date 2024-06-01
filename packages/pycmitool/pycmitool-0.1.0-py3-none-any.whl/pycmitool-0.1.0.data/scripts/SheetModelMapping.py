import pickle
import os
import pandas as pd
from SheetParser import parse_excel_sheets


def save_to_pickle(data, filename):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_from_pickle(filename):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except EOFError:
            print(f"Warning: {filename} is empty or corrupted. Returning an empty dictionary.")
            return {}
    return {}

def find_column(df, possible_names):
    """Utility function to find the correct column name."""
    for col in df.columns:
        if col in possible_names:
            return col
    return None

def identify_header_row(df, possible_names, max_rows=5):
    """Utility function to identify the header row by scanning the first few rows."""
    for i in range(min(max_rows, len(df))):
        row = df.iloc[i]
        for col in row:
            if pd.notna(col) and str(col) in possible_names:
                return i
    return -1

def create_bot_objects_from_excel(file_path):
    sheets = parse_excel_sheets(file_path)
    bots = load_from_pickle('pkl_files/bots.pkl')

    for sheet_name, df in sheets.items():
        header_row = identify_header_row(df, 'BOT Name')
        if header_row == -1:
            continue

        # Reassign DataFrame columns based on the identified header row
        df.columns = df.iloc[header_row].apply(lambda x: x if pd.notna(x) else '')
        df = df[header_row + 1:]
        df = df.reset_index(drop=True)

        bot_name_column = find_column(df, {'BOT Name'})
        if bot_name_column is None:
            continue

        for _, row in df.iterrows():
            bot_name = row.get(bot_name_column)
            if pd.notna(bot_name):
                bot_name = str(bot_name)
                if bot_name not in bots:
                    bots[bot_name] = {
                        'sysType': row.get(find_column(df, 'BOT SysType'), 0),
                        'description': row.get(find_column(df, 'Description'), ''),
                        'botName': bot_name,
                        'botId': row.get(find_column(df, 'BOT ID'), ''),
                        'botType': row.get(find_column(df, 'BOT Type'), ''),
                        'botIndex': row.get(find_column(df, 'BOT Index'), ''),
                        'botDescription': row.get(find_column(df, 'BOT Description'), ''),
                        'domainInformation': row.get(find_column(df, 'Domain Information'), ''),
                        'image': row.get(find_column(df, 'Image'), ''),
                        'longDescription': row.get(find_column(df, 'Long Description'), ''),
                        'summary': row.get(find_column(df, 'Summary'), ''),
                        'commonEquipment': row.get(find_column(df, 'Common Equipment'), ''),
                        'commonProcesses': row.get(find_column(df, 'Common Processes'), ''),
                        'commonOperations': row.get(find_column(df, 'Common Operations'), ''),
                        'customer': row.get(find_column(df, 'Customer'), 'Atomiton'),
                        'eatId': row.get(find_column(df, 'EAT ID'), '')
                    }

                # Update existing BOT with additional information
                bot = bots[bot_name]
                attributes = [
                    ('Description', 'description'),
                    ('BOT SysType', 'sysType'),
                    ('BOT ID', 'botId'),
                    ('BOT Type', 'botType'),
                    ('BOT Index', 'botIndex'),
                    ('BOT Description', 'botDescription'),
                    ('Domain Information', 'domainInformation'),
                    ('Image', 'image'),
                    ('Long Description', 'longDescription'),
                    ('Summary', 'summary'),
                    ('Common Equipment', 'commonEquipment'),
                    ('Common Processes', 'commonProcesses'),
                    ('Common Operations', 'commonOperations'),
                    ('Customer', 'customer'),
                    ('EAT ID', 'eatId')
                ]
                for possible_name, attr in attributes:
                    column = find_column(df, {possible_name})
                    if column and pd.notna(row.get(column)):
                        bot[attr] = row[column]

    save_to_pickle(bots, 'pkl_files/bots.pkl')
    return bots

def create_pod_objects_from_excel(file_path):
    sheets = parse_excel_sheets(file_path)
    pods = load_from_pickle('pkl_files/pods.pkl')

    for sheet_name, df in sheets.items():

        header_row = identify_header_row(df, 'POD Name')
        if header_row == -1:
            continue

        # Reassign DataFrame columns based on the identified header row
        df.columns = df.iloc[header_row].apply(lambda x: x if pd.notna(x) else '')
        df = df[header_row + 1:]  # Skip header row for data processing
        df = df.reset_index(drop=True)

        pod_name_column = find_column(df, {'POD Name'})
        if pod_name_column is None:
            continue

        for idx, row in df.iterrows():
            pod_name = row.get(pod_name_column)
            if pd.notna(pod_name):
                pod_name = str(pod_name)
                if pod_name not in pods:
                    pods[pod_name] = {
                        'sysType': row.get(find_column(df, 'POD SysType'), 0),
                        'description': row.get(find_column(df, 'Description'), ''),
                        'carbonSource': row.get(find_column(df, 'Carbon Source'), ''),
                        'podName': pod_name,
                        'customer': row.get(find_column(df, 'Customer'), 'Atomiton'),
                        'podCategory': row.get(find_column(df, 'POD Category'), ''),
                        'usability': row.get(find_column(df, 'Usability'), ''),
                        'domainInformation': row.get(find_column(df, 'Domain Information (POD)'), ''),
                        'image': row.get(find_column(df, 'Image (POD)'), ''),
                        'countrySpecific': row.get(find_column(df, 'Country Specific'), ''),
                        'referenceYear': row.get(find_column(df, 'Reference Year'), '')
                    }

                # Update existing POD with additional information
                pod = pods[pod_name]
                attributes = [
                    ('Description', 'description'),
                    ('POD SysType', 'sysType'),
                    ('Carbon Source', 'carbonSource'),
                    ('Customer', 'customer'),
                    ('POD Category', 'podCategory'),
                    ('Usability', 'usability'),
                    ('Domain Information (POD)', 'domainInformation'),
                    ('Image (POD)', 'image'),
                    ('Country Specific', 'countrySpecific'),
                    ('Reference Year', 'referenceYear')
                ]
                for possible_name, attr in attributes:
                    column = find_column(df, {possible_name})
                    if column and pd.notna(row.get(column)):
                        pod[attr] = row[column]

    save_to_pickle(pods, 'pkl_files/pods.pkl')
    return pods

def create_eat_objects_from_excel(file_path):
    sheets = parse_excel_sheets(file_path)
    eats = load_from_pickle('pkl_files/eats.pkl')

    for sheet_name, df in sheets.items():
        header_row = identify_header_row(df, 'EAT Name')
        if header_row == -1:
            continue

        df.columns = df.iloc[header_row].apply(lambda x: x if pd.notna(x) else '')
        df = df[header_row + 1:].reset_index(drop=True)

        eat_name_column = find_column(df, {'EAT Name'})
        if eat_name_column is None:
            continue

        for _, row in df.iterrows():
            eat_name = row.get(eat_name_column)
            if pd.notna(eat_name):
                eat_name = str(eat_name)
                if eat_name not in eats:
                    eats[eat_name] = {
                        'sysType': row.get(find_column(df, 'EAT SysType'), 0),
                        'description': row.get(find_column(df, 'Description'), ''),
                        'eatName': eat_name,
                        'eatFullName': row.get(find_column(df, '#EAT Full Name'), ''),
                        'ghgAmFullName': row.get(find_column(df, '#GHG-AM Full Name'), ''),
                        'ghgAmName': row.get(find_column(df, 'GHG-AM Name'), ''),
                        'mdDescription': row.get(find_column(df, 'MD Description'), ''),
                        'methodologyName': row.get(find_column(df, 'Methodology Name'), ''),
                        'carbonSource': row.get(find_column(df, 'Carbon Source'), ''),
                        'action': row.get(find_column(df, 'Action'), ''),
                        'activityDescription': row.get(find_column(df, 'Activity Description'), ''),
                        'reportedQuantity': row.get(find_column(df, 'Reported Quantity'), ''),
                        'rqDescription': row.get(find_column(df, 'Reported Quantity Description'), ''),
                        'rqAbbreviation': row.get(find_column(df, 'RQ Abbreviation'), ''),
                        'eaDataSource': row.get(find_column(df, 'EA Data Source'), '')
                    }

                eat = eats[eat_name]
                attributes = [
                    ('Description', 'description'),
                    ('EAT SysType', 'sysType'),
                    ('#EAT Full Name', 'eatFullName'),
                    ('#GHG-AM Full Name', 'ghgAmFullName'),
                    ('GHG-AM Name', 'ghgAmName'),
                    ('MD Description', 'mdDescription'),
                    ('Methodology Name', 'methodologyName'),
                    ('Carbon Source', 'carbonSource'),
                    ('Action', 'action'),
                    ('Activity Description', 'activityDescription'),
                    ('Reported Quantity', 'reportedQuantity'),
                    ('Reported Quantity Description', 'rqDescription'),
                    ('RQ Abbreviation', 'rqAbbreviation'),
                    ('EA Data Source', 'eaDataSource')
                ]
                for possible_name, attr in attributes:
                    column = find_column(df, {possible_name})
                    if column and pd.notna(row.get(column)):
                        eat[attr] = row[column]

    save_to_pickle(eats, 'pkl_files/eats.pkl')
    return eats

def create_dm_objects_from_excel(file_path):
    sheets = parse_excel_sheets(file_path)
    dms = load_from_pickle('pkl_files/dms.pkl')

    for sheet_name, df in sheets.items():
        header_row = identify_header_row(df, 'DM ID')
        if header_row == -1:
            continue

        df.columns = df.iloc[header_row].apply(lambda x: x if pd.notna(x) else '')
        df = df[header_row + 1:].reset_index(drop=True)

        dm_name_column = find_column(df, {'DM ID', 'DM'})
        if dm_name_column is None:
            continue

        for _, row in df.iterrows():
            dm_name = row.get(dm_name_column)
            if pd.notna(dm_name):
                dm_name = str(dm_name)
                if dm_name not in dms:
                    dms[dm_name] = {
                        'sysType': row.get(find_column(df, 'DM SysType'), 0),
                        'description': row.get(find_column(df, 'Description'), ''),
                        'dmType': row.get(find_column(df, 'DM Type'), ''),
                        'formula': row.get(find_column(df, 'Formula'), ''),
                        'notations': row.get(find_column(df, 'Notations'), ''),
                        'additionalVariables': row.get(find_column(df, 'Additional Variables'), ''),
                        'dmPref': row.get(find_column(df, 'DM Pref'), None),
                        'condition1': row.get(find_column(df, 'Condition 1'), ''),
                        'condition2': row.get(find_column(df, 'Condition 2'), ''),
                        'condition3': row.get(find_column(df, 'Condition 3'), ''),
                        'notes': row.get(find_column(df, 'Notes'), '')
                    }

                dm = dms[dm_name]
                attributes = [
                    ('Description', 'description'),
                    ('DM SysType', 'sysType'),
                    ('DM Type', 'dmType'),
                    ('Formula', 'formula'),
                    ('Notations', 'notations'),
                    ('Additional Variables', 'additionalVariables'),
                    ('DM Pref', 'dmPref'),
                    ('Condition 1', 'condition1'),
                    ('Condition 2', 'condition2'),
                    ('Condition 3', 'condition3'),
                    ('Notes', 'notes')
                ]
                for possible_name, attr in attributes:
                    column = find_column(df, {possible_name})
                    if column and pd.notna(row.get(column)):
                        dm[attr] = row[column]

    save_to_pickle(dms, 'pkl_files/dms.pkl')
    return dms

def create_bart_objects_from_excel(file_path):
    sheets = parse_excel_sheets(file_path)
    barts = load_from_pickle('pkl_files/barts.pkl')

    for sheet_name, df in sheets.items():
        header_row = identify_header_row(df, 'BART ID')
        if header_row == -1:
            continue

        df.columns = df.iloc[header_row].apply(lambda x: x if pd.notna(x) else '')
        df = df[header_row + 1:].reset_index(drop=True)

        bart_name_column = find_column(df, {'BART ID'})
        if bart_name_column is None:
            continue

        for _, row in df.iterrows():
            bart_name = row.get(bart_name_column)
            if pd.notna(bart_name):
                bart_name = str(bart_name)
                if bart_name not in barts:
                    barts[bart_name] = {
                        'sysType': row.get(find_column(df, 'BART SysType'), 0),
                        'description': row.get(find_column(df, 'Description'), ''),
                        'bartFullName': row.get(find_column(df, '#BART Full Name'), ''),
                        'carbonSource': row.get(find_column(df, 'Carbon Source'), ''),
                        'carbonSourceLifecycle': row.get(find_column(df, 'Carbon Source Lifecycle'), ''),
                        'activityDescription': row.get(find_column(df, 'Activity Description'), ''),
                        'measuredQuantity': row.get(find_column(df, 'Measured Quantity'), ''),
                        'measuredQuantityType': row.get(find_column(df, 'Measured Quantity Type'), ''),
                        'mqDescription': row.get(find_column(df, 'Measured Quantity Description'), ''),
                        'mqAbbreviation': row.get(find_column(df, 'MQ Abbreviation'), ''),
                        'unitAllowedValues': row.get(find_column(df, 'Unit Allowed Values'), '')
                    }

                bart = barts[bart_name]
                attributes = [
                    ('Description', 'description'),
                    ('BART SysType', 'sysType'),
                    ('#BART Full Name', 'bartFullName'),
                    ('Carbon Source', 'carbonSource'),
                    ('Carbon Source Lifecycle', 'carbonSourceLifecycle'),
                    ('Activity Description', 'activityDescription'),
                    ('Measured Quantity', 'measuredQuantity'),
                    ('Measured Quantity Type', 'measuredQuantityType'),
                    ('Measured Quantity Description', 'mqDescription'),
                    ('MQ Abbreviation', 'mqAbbreviation'),
                    ('Unit Allowed Values', 'unitAllowedValues')
                ]
                for possible_name, attr in attributes:
                    column = find_column(df, {possible_name})
                    if column and pd.notna(row.get(column)):
                        bart[attr] = row[column]

    save_to_pickle(barts, 'pkl_files/barts.pkl')
    return barts

def GetAllX(data_type):
    file_map = {
        'bots': 'pkl_files/bots.pkl',
        'pods': 'pkl_files/pods.pkl',
        'eats': 'pkl_files/eats.pkl',
        'dms': 'pkl_files/dms.pkl',
        'barts': 'pkl_files/barts.pkl'
    }

    if data_type in file_map:
        return load_from_pickle(file_map[data_type])
    else:
        raise ValueError("Invalid data type specified. Choose from 'bots', 'pods', 'eats', 'dms', or 'barts'.")

# Example usage
if __name__ == "__main__":
    file_path = 'System Data Authoring_Oct 2023.xlsx'
    bots = create_bot_objects_from_excel(file_path)
    pods = create_pod_objects_from_excel(file_path)
    eats = create_eat_objects_from_excel(file_path)
    dms = create_dm_objects_from_excel(file_path)
    barts = create_bart_objects_from_excel(file_path)
    
