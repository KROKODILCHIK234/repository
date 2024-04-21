from pathlib import Path
from datetime import datetime
import os
import json
import uuid
import sys

sys.path.append(os.path.join(Path(__file__).parent,'src'))

from error_proxy import error_proxy
from pathlib import Path
from storage.storage import storage

from Logic.storage_prototype import storage_prototype
from src.Logic.Reporting.Json_convert.reference_conventor import reference_conventor
from exceptions import argument_exception
from src.Logic.process_factory import process_factory
from src.Logic.storage_observer import storage_observer
from src.models.event_type import event_type

#для референсов
from src.storage.storage_turn_model import storage_turn_model
from models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.nomenclature_group_model import nomenclature_group_model
from models.reciepe_model import reciepe_model
from src.storage.storage_factory import storage_factory
from storage.storage_journal_row import storage_journal_row
from src.storage.storage_journal_transaction import storage_journal_transaction
from src.Logic.services.abstract_service import abstract_sevice

#PERENESTI I ZAMENIT MAIN

class post_processing_service(abstract_sevice):

    __nomenclature=None
    __storage=None
    



    def __init__(self, data: list):
        super().__init__(data)
        self.__storage=storage()
        storage_observer.observers.append(self)



    @property
    def nomenclature_id(self):
        return self.__nomenclature
    

    @nomenclature_id.setter
    def nomenclature_id(self,nom_id:uuid.UUID):
        if not isinstance(nom_id,uuid.UUID):
            raise argument_exception("неверный тип аргумента")
        storage_observer.observers.append(self)
        self.__nomenclature=nom_id


    def handle_event(self, handle_type: str):
        super().handle_event(handle_type)

        if handle_type==event_type.deleted_nomenclature():
            self.clear_reciepe()
            self.clear_journal()


    def clear_reciepe(self):

        key=storage.reciepe_key()
        for index,cur_rec in enumerate(self.__storage.data[key]):
            for cur_id in list(cur_rec.ingridient_proportions.keys()):
                print(cur_id==self.__nomenclature)
                if self.__nomenclature==cur_id:
                    res=cur_rec.ingridient_proportions
                    res.pop(self.__nomenclature )
                    storage().data[key][index].ingridient_proportions=res 
        

    def clear_journal(self):
        key=storage.journal_key()
        res=[]
        for cur_line in (self.__storage.data[key]):
            if cur_line.nomenclature.id!=self.__nomenclature:
                res.append(cur_line)

        self.__storage.data[key]=res
        storage_observer.raise_event(event_type.changed_block_period())
