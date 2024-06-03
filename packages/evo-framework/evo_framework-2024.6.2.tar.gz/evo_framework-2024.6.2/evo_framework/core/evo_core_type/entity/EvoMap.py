
class EvoMap(object):
    def __init__(self):
        self.__dictionary = {}

    def doSet(self, eObject):
        self.__dictionary[eObject.id] = eObject

    def doGet(self, id):
        return self.__dictionary.get(id)

    def doDel(self, id):
        if self.__dictionary[id] is not None:
            self.__dictionary.pop(id)
            
    def doDelAll(self):
        self.__dictionary.clear()
        
    def items(self):
        return self.__dictionary.items()
    
    def keys(self):
        return self.__dictionary.keys()
    
    def values(self):
        return self.__dictionary.values()
    
        
    def __str__(self) ->str:
        return f"{self.__dictionary.keys()}"

'''
import json
class EvoMapEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, EvoMap):
            return obj.name  # {'name': obj.name, 'dictionary': obj.dictionary}
        return json.JSONEncoder.default(self, obj)

'''