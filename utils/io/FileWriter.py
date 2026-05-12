import json
import os

from utils.json.json_encoder import *


class FileWriter():
    """Utility class to write contents to file"""
    
    @staticmethod
    def write(file_path:str, content:str):
        """Write content string to file.
        """
        try:
            with open(file=f"{file_path}", mode="x+t", encoding="utf-8") as file:
                file.write(content)
        except FileExistsError: # If file exist, overwrite instead.
            print("File already exists, overwriting file instead.")
            with open(file=f"{file_path}", mode="w+t", encoding="utf-8") as file:
                file.write(content)
        # file.close() # Should not be required, is already handled by the with ... as file construct

    @staticmethod
    def writeJSON(o, path:str):
        try:
            with open(file=f"{path}", mode="x+t", encoding="UTF-8") as file:
                json.dump(obj=o, fp=file, indent=2 ,cls=USDMEncoder)
        except FileExistsError:
            # File already exists, overwriting
            with open(file=f"{path}", mode="w+t", encoding="UTF-8") as file:
                json.dump(obj=o, fp=file, indent=2 ,cls=USDMEncoder)
        finally:
            # Open saved file
            os.startfile(f"{path}")
            
        