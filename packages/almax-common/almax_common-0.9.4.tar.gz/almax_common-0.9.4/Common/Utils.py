import os;
from datetime import datetime;

now = datetime.now();

def CalculateDestinationFolder(source: str) -> str:
    destination = CleanPath(source, '/').split('/');

    if  destination[0] == 'H:':
        destination[0] = 'Q:';
    elif destination[0] == 'C:':
        destination[3] = "Test";
    else:
        return '';

    return '/'.join(destination);

def CleanPath(path: str, cleanString: str) -> str:
    return path.replace("\\", cleanString).replace('/', cleanString);

def GetSubFolders(folder: str) -> list:
    return [ f.path for f in os.scandir(folder) if f.is_dir() ];

def GetSubFolders(folder: str, level: int) -> list:
    subfolders = [];
    level -= 1;
    if level == 0:
        content = [ f.path for f in os.scandir(folder) if f.is_dir() ];
        if len(content) > 0:
            return content;
        else:
            return [folder];
   
    content = [ f for f in os.scandir(folder) if f.is_dir() ];
    if len(content) > 0:
        for element in content:
            subfolders += GetSubFolders(element.path, level);
    else:
        return [folder];

    return subfolders;

def GetSubFoldersWithFiles_Robocopy(folder: str, level: int) -> list:
    folderForFiles = [];
    level -= 1;
    fileCheckedOnce = False;
    if level == 0:
        for content in os.scandir(folder):
            if content.is_file():
                return [folder];
        return [];
   
    for content in os.scandir(folder):
        if (not fileCheckedOnce) and content.is_file():
            folderForFiles += [folder];
            fileCheckedOnce = True;
        elif content.is_dir():
            folderForFiles += GetSubFoldersWithFiles_Robocopy(content.path, level);

    return folderForFiles;

def GetFolderFiles(folder: str) -> list:
    return [ f.path for f in os.scandir(folder) if f.is_file() ];

def HasFiles(folder: str) -> bool:
    files = os.listdir(folder);
    return len(files) > 0;
   
def GetRobocopyCommand(source: str, elaboration: int, operation:int, onlyFiles=False, customFolder: str = '', checkIfExists: list = []) -> list:
    destination = CalculateDestinationFolder(source);
    destinationLog = destination.split("/");
    destinationLog = destinationLog[-1];

    logPath = f"{customFolder}{destinationLog.replace(":", "").replace("/", "_") + ("_Files" if onlyFiles else "") + ".log"}";
    i = 0;
    while logPath in checkIfExists:
        i+=1;
        logPath = f"{customFolder}{destinationLog.replace(":", "").replace("/", "_").replace(" ", "_") + ("_Files" if onlyFiles else "") + "_" + str(i) + ".log"}";
    checkIfExists.append(logPath);

    command = [
        "Robocopy",
        source,
        destination,
        f"/LOG:{logPath}"
    ];

    if elaboration in [32, 64, 128]:
        command.append(f"/MT:{elaboration}");
    if not onlyFiles:
        command.append("/E");
    if operation == 1:
        command.append("/MOVE");

    return [command, checkIfExists];

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

def CalculateTime(start: datetime):
    return datetime.now() - start;

def TimeToString(time: datetime) -> str:
    seconds = time.total_seconds();
    minutes = seconds // 60;
    hours = minutes // 60;
    days = hours // 24;
    return f"{round(days)} Days = {round(hours)} Hours = {round(minutes)} Minutes = {round(seconds, 2)} Seconds";

def CheckStringInFile(file_path, target_string):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if target_string in line:
                    return True;
        return False;
    except FileNotFoundError:
        return False;