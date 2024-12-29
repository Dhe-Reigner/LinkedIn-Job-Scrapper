import asyncio
import platform
import argparse

from .main import main

def get_args():
    # ArgumentParser object to capture command-line arguments
    parser = argparse.ArgumentParser(description="Crawl LinkedIn Job Listings")
    
    # Define the arguments
    parser.add_argument("--title", type=str, required=True, help="Job title")
    parser.add_argument("--location", type=str, required=True, help="Job location")
    parser.add_argument("--data_name", type=str, required=True, help="Name for the output CSV file")
    
    # Parse the arguments
    return parser.parse_args()

if __name__ == '__main__':
    # if platform.system == 'Windows':
    #     # This mitigates a warning raised by curl-cffi. If you do not need to use curl-impersonate, you may remove this.
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    args = get_args()
    
    asyncio.run(main(args.title, args.location, args.data_name))
