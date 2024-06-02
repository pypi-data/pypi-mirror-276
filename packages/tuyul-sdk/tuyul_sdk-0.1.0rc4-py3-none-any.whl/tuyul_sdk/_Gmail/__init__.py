import base64
from typing import Any, List, Union

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .Utils import Utils

class ServiceError(Exception): ...

class Gmail:

    def __init__(self, Service: Any = None) -> None:
        if not Service:
            raise ServiceError('Connection services required')
        self.Service = Service

    @classmethod
    def Connections(cls, Auth: str):
        return cls(build('gmail', 'v1', credentials=Credentials(token=Auth)))
    
    @property
    def ListEmail(self):
        return Utils.Response.ListEmail(self.Services.users().messages().list(userId='me', q='is:unread').execute())
    
    @property
    def Contents(self):
        return Utils.Response.Contents(self.Services.users().messages().get(userId='me', id=self.Messageid, format='full').execute())
    
    @property
    def Unread(self):
        return Utils.Response.Unread(self.Services.users().messages().modify(userId='me', id=self.Messageid,body={ 'removeLabelIds': ['UNREAD']}).execute())
    
    def getTitle(self, headers: List[Utils.Response.Headers]) -> Union[str, None]:
        subject = None
        for header in headers:
            if header.name == 'Subject':
                subject = header.value
                break
        return subject
    
    def getDate(self, headers: List[Utils.Response.Headers]) -> Union[str, None]:
        subject = None
        for header in headers:
            if header.name == 'Date':
                subject = header.value
                break
        return subject
    
    @staticmethod
    def data_encoder(text)-> str:
        message = None
        if len(text)>0:
            message = base64.urlsafe_b64decode(text)
            message = str(message, 'utf-8')
        return message
    
    def ReadMessage(self, payload: Utils.Response.Payload) -> Union[str, None]:
        message = None
        if payload.body is not None:
            message = payload.body.data
            message = self.data_encoder(message)
        elif payload.parts is not None:
            message = payload.parts[0].body.data
            message = self.data_encoder(message)
        else:
            message = None
        return message