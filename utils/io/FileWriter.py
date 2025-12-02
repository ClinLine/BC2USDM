import json

from utils.json.json_encoder import USDMEncoder


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
        file.close()

    @staticmethod
    def writeJSON(o, path:str):
        try:
            with open(file=f"{path}", mode="x+t", encoding="UTF-8") as file:
                json.dump(o, file)
        except FileExistsError:
            # File already exists, overwriting
            with open(file=f"{path}", mode="w+t", encoding="UTF-8") as file:
                
                # print(json.dumps(o,cls=USDMEncoder, check_circular=True))
                json.dump(o, file, cls=USDMEncoder)
        