from peewee import CharField
from peewee import IntegerField

from models.base import BaseModel

class ClassModel(BaseModel):
    chat_id = IntegerField(null=False)
    class_name = CharField(null=False)
    skipped_classes = IntegerField(default=0)
    skipped_classes_limit = IntegerField(null=False)

    def list_by_chat(self, chat_id):
        return ClassModel.get(ClassModel.chat_id == chat_id)
