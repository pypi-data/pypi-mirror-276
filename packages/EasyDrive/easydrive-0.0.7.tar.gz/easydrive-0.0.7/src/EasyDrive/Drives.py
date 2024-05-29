from math import e
from os import PathLike
import os.path
from typing import Union
from .Exceptions import InvaildCredentials, DrivePathException
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .FileSystemTypes import *
from google.oauth2.credentials import Credentials
def one_time_login(credentialsFile: str = "credentials.json")->Credentials:
        SCOPES = [
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/docs',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/drive.file'
    ]
        flow = InstalledAppFlow.from_client_secrets_file(credentialsFile, SCOPES)
        creds = flow.run_local_server(port=0)
        return creds # type: ignore
def login(tokenFile: str = "token.json", credentialsFile: str = "credentials.json") -> Credentials:
    """
    Logs in to the Google API and returns credentials.

    Args:
        tokenFile (PathLike): The path to the token file. Defaults to "token.json".
        credentialsFile (PathLike): The path to the credentials file. Defaults to "credentials.json".

    Returns:
        Credentials: The credentials object for the Google API.

    Raises:
        InvaildCredentials: If no valid credentials file is found.
    """
    creds = None
    SCOPES = [
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/docs',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/drive.file'
    ]
    if os.path.exists(tokenFile):
        creds = Credentials.from_authorized_user_file(tokenFile, SCOPES)
    if not creds or not creds.valid:
        if not os.path.exists(credentialsFile):
            raise InvaildCredentials("No credentials file found or the path was invalid")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentialsFile, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(tokenFile, "w") as token:
                token.write(creds.to_json())
    return creds # type: ignore

class Drive:
    def __init__(self, creds) -> None:
        """
        Initializes a Google Drive instance.

        Args:
            creds: Credentials object for Google Drive API.
        """
        self.__service = build("drive", "v3", credentials=creds)
        # self.__currentDir = "/"
        
        self.__root: RootFolder = RootFolder(self.__service)
        self.__currentFolder:Folder = self.__root
        self.__currentFolder = self.__root
    def cd(self, path: str) -> None:
        """
        Changes the current directory.

        Args:
            path (str): The path to change to.

        Raises:
            DrivePathException: If the path is invalid.
        """
        
        folder = self.__transverse_path(path)
        if not isinstance(folder, Folder):
            raise DrivePathException(f"No such directory as {folder}")
        self.__currentFolder = folder
        if path in '..':path = path.replace("..", self.__getParent().name())

    def __transverse_path(self, path: str) -> Folder:
        """
        Transverses the path to find the target folder .

        Args:
            path (str): The path to transverse.

        Returns:
            Folder object at the end of the path.

        Raises:
            DrivePathException: If the path is invalid.
        """
        parts = path.split("/") 
        if path.startswith("/"):
            current_folder = self.__root
        else:
            current_folder = self.__currentFolder if not path.startswith("..") else self.__currentFolder.getParent()
        if parts[0] == "" or parts[0] == "..":
            parts.pop(0)
        for part in parts:
            if current_folder is not None:
                current_folder = current_folder.get_folder_by_name(part)
            if current_folder is None:
                raise DrivePathException(f"No such directory {part}")
        if current_folder is None:
            raise DrivePathException(f"Invalid path: {path}")
        return current_folder

    def __getParent(self) -> Folder:
        """
        Retrieves the parent folder of the current directory.

        Returns:
            Parent Folder object or None if in root.
        """
        
        if self.__currentFolder.name() != "/":
            parts = self.getCurrentFolder().split("/")
            parts.pop()
            parts.pop()
            if len(parts) > 1: return self.__root
            parent_path = "/".join(parts)
            return self.__transverse_path(parent_path)
        else:
            return self.__root

    def dir(self, path: str = None) -> list[Union[File, Folder]]: # type: ignore
        """
        Lists the contents of the given path or the current folder.

        Args:
            path (str, optional): The path to list contents of. Defaults to None.

        Returns:
            list of File and Folder objects in the specified path or current folder.

        Raises:
            DrivePathException: If the path is invalid.
        """
        
        if path:
            target = self.__transverse_path(path)
        else:
            target = self.__currentFolder

        if isinstance(target, Folder) or issubclass(type(target),Folder):
            files, folders = target.get_files(), target.get_folders()
        else:
            raise DrivePathException(f"No such directory as {path}")

        return files + folders
    
    def file(self, path: str,type='text/plain') -> File:
        """
        get's a file
        Creates a file at the given path if one does Not exist.

        Args:
            path (str): The path where the file should be created.
            type(str, optional): The file type that you want to use to create a folder if none exist defaults to plain text

        Returns:
            the file
        """
        
        path = path.replace("\\", "/")
        parts = path.split("/")
        filename = parts.pop()

        if parts:
            folder_path = "/".join(parts)
            folder = self.__transverse_path(folder_path)
            if not isinstance(folder, Folder):
                raise DrivePathException(f"No such directory: {folder_path}")
        else:
            folder = self.__currentFolder

        # Check if the file already exists
        try:
            existing_file = next((f for f in folder.get_files() if f.__str__() == filename), None)
        except TypeError: existing_file=False
        if existing_file:
            return folder.get_file_by_name(filename) # type: ignore

        # Create the file
        file_metadata = {
            'name': filename,
            'parents': [folder.get_id()],
            'mimeType':type
        }
        self.__service.files().create(body=file_metadata, fields='id').execute()
        return folder.get_file_by_name(filename) # type: ignore
    def mkdir(self, path: str) -> None:
        """
        Creates a folder at the given path if one does not already exist.

        Args:
            path (str): The path where the folder should be created.

        Raises:
            DrivePathException: If the path is invalid or the folder already exists.
        """
        
        path = path.replace("\\", "/")
        parts = path.split("/")
        folder_name = parts.pop()

        if parts:
            parent_folder_path = "/".join(parts)
            parent_folder = self.__transverse_path(parent_folder_path)
        else:
            parent_folder = self.__currentFolder if self.__currentFolder else self.__root

        # Check if the folder already exists
        existing_folder = next((f for f in parent_folder.get_folders() if f.__str__() == folder_name), None)
        if existing_folder:
            raise DrivePathException(f"Folder '{folder_name}' already exists at path '{path}'.")

        # Create the folder
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder.get_id()]
        }
        self.__service.files().create(body=folder_metadata, fields='id').execute()
    def rmdir(self, path: str) -> None:
            
        path = path.replace("\\", "/")
        parts = path.split("/")
        folder_name = parts.pop()

        if parts:
            parent_folder_path = "/".join(parts)
            parent_folder = self.__transverse_path(parent_folder_path)
        else:
            parent_folder = self.__currentFolder if self.__currentFolder else self.__root
        folder=parent_folder.get_folder_by_name(folder_name)
        if not folder:raise DrivePathException(f"Folder '{folder_name}' does not exist at path '{path}'")
        folder.delete()
    def getCurrentFolder(self)->str:
        """
        Gets the path to the current folder
        Returns:
            the path to the current folder
        """
        folders:list[Folder]=[self.__currentFolder]
        parent=self.__currentFolder.getParent()
        if parent is not None and not isinstance(parent, RootFolder):
            folders.append(parent)
        while parent is not None and not isinstance(parent, RootFolder):
            parent=parent.getParent()
            if parent is not None and not isinstance(parent,RootFolder):
                folders.append(parent)
        folders.reverse()
        path=""
        for folder in folders:
            path+="/"
            if isinstance(folder,RootFolder):continue
            path+=folder.name()

        return path
    def exists(self,path:str)->bool:
        """
        check if the path exist
        Args:
            path(str):the path you want to check
        Returns:
            True if the path exist else returns False
        """
        try:
           folder=self.__transverse_path(path)
           return True
        except DrivePathException:
            try:
                parts=path.split("/")
                if len(parts)==1:
                    if path in [f.name() for f in self.__currentFolder.get_files()] or path in [f.name() for f in self.__currentFolder.get_folders()]:return True
                    else: return False
                file = parts.pop()
                file = file if file !="" else parts.pop()
                path = path.replace(file,"")
                folder=self.__transverse_path(path)
                if file in [f.name() for f in folder.get_files()]:return True
                else:return False
            except DrivePathException:return False
