def PrintBytes(size: int) -> str:
    if size > 1024:
        size = round(size / 1024, 2);
        if(size > 1024):
            size = round(size / 1024, 4);
            if(size > 1024):
                size = round(size / 1024, 8);
                if(size > 1024):
                    size = round(size / 1024, 16);
                    return f"{size} TB";
                else:
                    return f"{size} GB";
            else:
                return f"{size} MB";
        else:
            return f"{size} KB";
   
    return f"{size} B";

def CheckStringInFile(file_path, target_string):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if target_string in line:
                    return True;
        return False;
    except FileNotFoundError:
        return False;

def CleanArrayFromEmptyString(array: list) -> list:
    return [string for string in array if string != ""];

def ReadFile(file_path: str) -> list:
    with open(file_path, 'r') as file:
        lines = file.readlines();
    return lines;