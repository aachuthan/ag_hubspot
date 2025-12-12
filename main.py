import argparse
import sys
from hubspot_data_gen.generators import ContactGenerator, CompanyGenerator, DealGenerator, TicketGenerator
from hubspot_data_gen.inserter import HubSpotInserter

def main():
    parser = argparse.ArgumentParser(description="Generate and insert dummy data into HubSpot.")
    parser.add_argument("--object", "-o", type=str, required=True, 
                        choices=["contacts", "companies", "deals", "tickets"],
                        help="The object type to generate data for.")
    parser.add_argument("--count", "-c", type=int, default=10, 
                        help="Number of records to generate.")
    parser.add_argument("--dry-run", action="store_true", 
                        help="Generate data but do not insert into HubSpot.")

    args = parser.parse_args()

    # Select Generator
    if args.object == "contacts":
        generator = ContactGenerator()
    elif args.object == "companies":
        generator = CompanyGenerator()
    elif args.object == "deals":
        generator = DealGenerator()
    elif args.object == "tickets":
        generator = TicketGenerator()
    else:
        print("Invalid object type selected.")
        sys.exit(1)

    # Generate Data
    print(f"Generating {args.count} {args.object}...")
    data = generator.generate(args.count)
    
    if args.dry_run:
        print("Dry run enabled. Example record:")
        print(data[0] if data else "No data generated.")
        print(f"Total records generated: {len(data)}")
    else:
        # Insert Data
        inserter = HubSpotInserter()
        try:
            inserter.batch_insert(args.object, data)
        except Exception as e:
            print(f"Failed to insert data: {e}")

if __name__ == "__main__":
    main()
