import argparse
import os

class SharedProgram:
    def __init__(self, program_name="", program_desc="") -> None:
        self.args = argparse.ArgumentParser(
            prog=program_name,
            description=program_desc)
        
        self.name = program_name
        self.description = program_desc
        
        self.args.add_argument(
            "url", 
            type=str, 
            help="root url to use")
        
        self.args.add_argument(
            "string",
            type=str, 
            help="search string")
        
        self.args.add_argument(
            "--extension", 
            action="store_true", 
            help="use if search string is a file extension")
        
        self.args.add_argument(
            "--ignore-keyword", 
            help="will ignore any path containing this keyword")
        
        self.args.add_argument(
            "--ignore-case", 
            action="store_true", 
            help="ignore case for seach and ignore terms")
        
        self.args.add_argument(
            "--randomise-result", 
            action="store_true", 
            help="if true, list of results found will be in randomised order")
        
        self.args.add_argument(
            "--randomise-result-count", 
            type=int, 
            default=-1, 
            help="how many results to collect from randomised list. -1 for whole list")
        
    def parse_args(self):
        return self.args.parse_args()
    
    def print_preamble(self):
        print(f"\n Program: {self.name}\n Arguments: {' '.join(f'{k}={v}' for k, v in vars(self.args.parse_args()).items())}")