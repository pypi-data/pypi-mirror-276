import argparse
import pprint
from SheetParser import parse_excel_sheets
from SheetModelMapping import GetAllX

file_path = 'System Data Authoring_Oct 2023.xlsx'  # Update this path accordingly

# Load data from the Excel file
bots = GetAllX('bots')
pods = GetAllX('pods')
eats = GetAllX('eats')
dms = GetAllX('dms')
barts = GetAllX('barts')

def list_all_objects(objects_dict, object_type):
    print(f"All {object_type} Names:")
    for name in objects_dict.keys():
        print(name)

def list_all_details(objects_dict, object_type):
    print(f"All {object_type} Details:")
    for name, obj in objects_dict.items():
        print(f"{object_type} Name: {name}")
        pprint.pprint(obj, indent=2)
        print()

def list_details_by_name(objects_dict, name, object_type):
    if name in objects_dict:
        print(f"{object_type} Details for '{name}':")
        pprint.pprint(objects_dict[name], indent=2)
    else:
        print(f"{name} '{object_type}' not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI for managing BOTs, PODs, EATs, DMs, and BARTs.")
    
    subparsers = parser.add_subparsers(dest="command")

    # Define commands for listing all names
    list_parser = subparsers.add_parser("list", help="List all names of a given type.")
    list_parser.add_argument("--BOT", action='store_true', help="List all BOT names.")
    list_parser.add_argument("--POD", action='store_true', help="List all POD names.")
    list_parser.add_argument("--EAT", action='store_true', help="List all EAT names.")
    list_parser.add_argument("--DM", action='store_true', help="List all DM names.")
    list_parser.add_argument("--BART", action='store_true', help="List all BART names.")
    
    # Define commands for listing all details
    listdetails_parser = subparsers.add_parser("listdetails", help="List all details of a given type or details of a specific name.")
    listdetails_parser.add_argument("--BOT", action='store_true', help="List all BOT details.")
    listdetails_parser.add_argument("--POD", action='store_true', help="List all POD details.")
    listdetails_parser.add_argument("--EAT", action='store_true', help="List all EAT details.")
    listdetails_parser.add_argument("--DM", action='store_true', help="List all DM details.")
    listdetails_parser.add_argument("--BART", action='store_true', help="List all BART details.")
    listdetails_parser.add_argument("name", nargs='?', type=str, help="The name of the object (optional).")

    args = parser.parse_args()

    if args.command == "list":
        if args.BOT:
            list_all_objects(bots, "BOT")
        elif args.POD:
            list_all_objects(pods, "POD")
        elif args.EAT:
            list_all_objects(eats, "EAT")
        elif args.DM:
            list_all_objects(dms, "DM")
        elif args.BART:
            list_all_objects(barts, "BART")
    elif args.command == "listdetails":
        if args.name:
            if args.BOT:
                list_details_by_name(bots, args.name, "BOT")
            elif args.POD:
                list_details_by_name(pods, args.name, "POD")
            elif args.EAT:
                list_details_by_name(eats, args.name, "EAT")
            elif args.DM:
                list_details_by_name(dms, args.name, "DM")
            elif args.BART:
                list_details_by_name(barts, args.name, "BART")
        else:
            if args.BOT:
                list_all_details(bots, "BOT")
            elif args.POD:
                list_all_details(pods, "POD")
            elif args.EAT:
                list_all_details(eats, "EAT")
            elif args.DM:
                list_all_details(dms, "DM")
            elif args.BART:
                list_all_details(barts, "BART")
    else:
        parser.print_help()
