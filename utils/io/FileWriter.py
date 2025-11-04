class FileWriter():
    """Utility class to write contents to file"""
    
    @staticmethod
    def write(file_path:str, content:str):
        print(f"attempting to write:\n{content}")
        print(f"To file:\n{file_path}")
        
        with open(file=f"{file_path}", mode="x", encoding="utf-8") as file:
            file.write(content)
            file.close()