import io
from tkinter import NO
from typing import Union
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload
from googleapiclient.errors import HttpError
from .Exceptions import DrivePathException
from googleapiclient.discovery import Resource
class Folder:
    def __init__(self, folder_name:str, folder_id:str, service:Resource, parent:'Folder'):
        """
        Initialize a Folder instance.

        Args:
            folder_name (str): The name of the folder.
            folder_id (str): The unique ID of the folder.
            service (googleapiclient.discovery.Resource): The Google Drive service instance.
            parent (Folder):the parent Folder
        """
        self.__folder_name = folder_name
        self.__id = folder_id
        self.__service = service
        self.__parent = parent
    def get_id(self):
        return self.__id
    def getParent(self)->'Folder':
        return self.__parent
    def name(self):return self.__folder_name
    def get_files(self)->list['File']:
        """
        Get all files in the folder.

        Returns:
            list[File]: List of File objects in the folder.
        """
        query = f"'{self.__id}' in parents and mimeType!='application/vnd.google-apps.folder'"
        try:
            files=[]
            results = self.__service.files().list(q=query, fields="files(id, name)").execute() # type: ignore
            items = results.get('files', [])
            for item in items:
                item=dict(item)
                if not item.get('mimeType') or not item['mimeType'].startswith('application/vnd.google-apps.'):
                        file = File(item['name'], item['id'], self.__service)
                else: 
                        file = Doc(item['name'], item['id'], self.__service)
                files.append(file)
            return files
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    def get_folders(self)->list['Folder']:
        """
        Get all subfolders in the folder.

        Returns:
            list[Folder]: List of Folder objects in the folder.
        """
        query = f"'{self.__id}' in parents and mimeType='application/vnd.google-apps.folder'"
        try:
            results = self.__service.files().list(q=query, fields="files(id, name)").execute() # type: ignore
            items = results.get('files', [])
            return [Folder(item['name'], item['id'], self.__service,self) for item in items]
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    def get_folder_by_name(self, name:str)->Union['Folder',None]:
        """
        Gets a folder by name
        Args:
            name(str)
        Returns:
            Folder or None if A folder was found return the folder
        """
        for folder in self.get_folders():
            if folder.name() == name:
                return folder
        return None
    
    def get_file_by_name(self, name:str)->Union['File',None]:
        """
        Gets a file by name
        Args:
            name(str)
        Returns:
            File or None if A File was found return the File if not return None
        """
        for file in self.get_files():
            if file.name() == name:
                return file
        return None
    def rename(self, new_foldername):
        """
        Rename the folder.

        Args:
            new_foldername (str): The new name for the folder.
        """
        try:
            file_metadata = {'name': new_foldername}
            self.__service.files().update(fileId=self.__id, body=file_metadata).execute() # type: ignore
            self.__folder_name = new_foldername
        except HttpError as error:
            print(f"An error occurred: {error}")

    def delete(self):
        """
        Delete the folder from Google Drive.

        Raises:
            HttpError: An error occurred while deleting the folder.
        """
        try:
            self.__service.files().delete(fileId=self.__id).execute() # type: ignore
        except HttpError as error:
            raise DrivePathException(f"An error occurred: {error}")
    
    def __str__(self):
        return self.__folder_name

    def __repr__(self) -> str:
        return str(self)


class File:
    def __init__(self, filename:str, file_id:str, service:Resource):
        """
        Initialize a File instance.

        Args:
            filename (str): The name of the file.
            file_id (str): The unique ID of the file.
            service (googleapiclient.discovery.Resource): The Google Drive service instance.
        """
        self.__filename = filename
        self.__id = file_id
        self.__service = service
    def name(self):return self.__filename
    def rename(self, new_filename):
        """
        Rename the file.

        Args:
            new_filename (str): The new name for the file.
        """
        try:
            file_metadata = {'name': new_filename}
            self.__service.files().update(fileId=self.__id, body=file_metadata).execute() # type: ignore
            self.__filename = new_filename
        except HttpError as error:
            print(f"An error occurred: {error}")

    def delete(self):
        """
        Delete the file from Google Drive.
        """
        try:
            self.__service.files().delete(fileId=self.__id).execute() # type: ignore
        except HttpError as error:
            print(f"An error occurred: {error}")

    def read(self) -> bytes:
        """
        Read the contents of the file.

        Returns:
            bytes: The contents of the file.
        """
        try:
            request = self.__service.files().get_media(fileId=self.__id) # type: ignore
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)
            return fh.read()
        except HttpError as error:
            print(f"An error occurred: {error}")
            return b''

    def write(self, content: bytes, mime_type='application/octet-stream'):
        """
        Write contents to the file.

        Args:
            content (bytes): The content to write to the file.
            mime_type (str): The MIME type of the file content.
        """
        try:
            media = MediaIoBaseUpload(io.BytesIO(content), mimetype=mime_type)
            self.__service.files().update(fileId=self.__id, media_body=media).execute() # type: ignore
        except HttpError as error:
            print(f"An error occurred: {error}")

    def __str__(self) -> str:
        return self.__filename

    def __repr__(self) -> str:
        return str(self)
class Doc(File):
    def __init__(self, filename, file_id, service):
        """
        Initialize a Doc instance.

        Args:
            filename (str): The name of the document.
            file_id (str): The unique ID of the document.
            service (googleapiclient.discovery.Resource): The Google Drive service instance.
        """
        super().__init__(filename, file_id, service)
        self.__service=service
        self.__id=file_id
    def rename(self, new_filename):
        """
        Rename the document.

        Args:
            new_filename (str): The new name for the document.
        """
        super().rename(new_filename)

    def delete(self):
        """
        Delete the document from Google Drive.
        """
        super().delete()

    def read(self) -> bytes:
        """
        Read the contents of the document and export it as a DOCX file.

        Returns:
            bytes: The contents of the document as a DOCX file.
        """
        try:
            request = self.__service.files().export_media(fileId=self.__id, mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document') # type: ignore
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)
            return fh.read()
        except HttpError as error:
            print(f"An error occurred: {error}")
            return b''
    def write(self, content: bytes):
        """
        Write contents to the document.

        Args:
            content (bytes): The content(DOCX file like bytes) to write to the document.
        """
        super().write(content, mime_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

class RootFolder(Folder):
    def __init__(self,service:Resource)->None:
       self.__service = service
    def __build(self):
         
        """
            Builds the initial list of folders and files.
        """
        files = []
        folders = []
        query = "mimeType='application/vnd.google-apps.folder'"
        results = self.__service.files().list(q=query, fields="nextPageToken, files(id, name)").execute() # type: ignore
        items = results.get('files', [])
        
        for item in items:
            folder = Folder(item['name'], item['id'], self.__service,self)
            folders.append(folder)
        query = (
            "mimeType!='application/vnd.google-apps.folder' and "
            "mimeType!='application/vnd.google-apps.spreadsheet' and "
            "mimeType!='application/vnd.google-apps.presentation' and "
            "mimeType!='application/vnd.google-apps.form' and "
            "mimeType!='application/vnd.google-apps.drawing' and "
            "mimeType!='application/vnd.google-apps.map' and "
            "mimeType!='application/vnd.google-apps.script' and "
            "mimeType!='application/vnd.google-apps.site' and "
            "mimeType!='application/vnd.google-apps.jam' and "
            "mimeType!='application/vnd.google-apps.shortcut'"
        )
        results = self.__service.files().list(q=query, fields="nextPageToken, files(id, name, mimeType)").execute() # type: ignore
        items = results.get('files', [])

        for item in items:
            if item['mimeType'].startswith('application/vnd.google-apps.'):
                file = Doc(item['name'], item['id'], self.__service)
            else:
                file = File(item['name'], item['id'], self.__service)
            files.append(file)
        self.__folders=folders
        self.__files=files
    def get_folders(self)->list[Folder]:
        self.__build()
        return self.__folders
    def get_files(self) -> list['File']:
        self.__build()
        return self.__files
    def get_id(self):
        return None
    def delete(self):raise NotImplementedError("Can't delete the root folder")
    def rename(self, new_foldername):raise NotImplementedError("Can't rename the root folder")
    def name(self):return '/'
    def getParent(self):
        return self
    
