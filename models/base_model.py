#!/usr/bin/python3
"""
Base module
"""

import uuid
import datetime
from models import storage

class BaseModel:
    """ Defines all common attributes/methods for other classes"""
    def __init__(self, id, created_at, updated_at):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def __str__(self):
        return '[{}] ({}) {}'.format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates instance attribute with the current datetime"""
        self.updated_at = datetime.datetime.now()
        # call save(self) method of storage
        storage.save()

    def to_dict(self):
        """ Returns all keys/values of __dict__ of the instance"""
        dict = self.__dict__.copy
        dict['__class__'] = self.__class__.__name__
        dict['created_at'] = self.created_at.isoformat()
        dict['updated_at'] = self.updated_at.isoformat()
        return dict

    def __init__(self, *args, **kwargs):
        """ Recreate instance variables of the dict representation"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
                    if key in ['created_at', 'updated_at']:
                        setattr(self, key, datetime.datetime.strptime
                                (value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    self.id = str(uuid.uuid4())
                    self.created_at = datetime.datetime.now()
                    storage.new(self)