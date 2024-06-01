
# ========================================================================================================================================
#                                                                                                                                       #
#                                 00000                                                                                                 #
#                                00   00                                                                                                #
#                 0000          0     0                                                                                                 #
#                800  007        0     0                                     0000                                                       #
#                0      7       00 00000                  4800000008         0  0                                      800008   6882    #
#                0     000  006 0 00                    580        08        0  0                                     80    0      8    #
#                800000  0000 00000                    28   00000   0000  0000  000000000000000000000000000000000    80  9  09  9  8    #
#                     000   0    00     8006           8   04   8000   0000  0        00        00              0    0   0   09 9  8    #
#                      0  0       0000000  083         8   8     8800   00  00  0000      0000   0   00  0000   0   00  000   0 9  8    #
#            58000800000          00    0    3         28  0088800 000  0   00  00 00     00 00  0  00   0000   0  00         089  8    #
#            8    00   00         00000     83          8     0     800    000   000   0   000   0  000         0  0   00000   08  8    #
#                  0000000      000   8000084           3880      008 00  00 0  0    0000      000  0 000   0   0  0  08   90   9  8    #
#            8     0     00000000                          68000008  00  00  000000000  00000000 0000 0  0000  00  0000     68088882    #
#            4800008         0  00                                   0   0                            00      00                        #
#                           000  000                                 00000                             00000000                         #
#                           0 0    0                                                                                                    #
#                           0      0                                                                                                    #
#                           00000000                                                                                                    #
#                                                                                                                                       #
# CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International       https://github.com/cyborg-ai-git     #
# ========================================================================================================================================

from evo_framework.core import *
import lz4.frame
from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap
from evo_framework.core.evo_core_api.entity import *

from evo_framework.core.evo_core_crypto import *
from evo_framework.core.evo_core_log import *
from evo_framework.core.evo_core_key import *
from evo_framework.core.evo_core_system import *
from evo_framework.core.evo_core_binary.utility.IuBinary import IuBinary
from PIL import Image
import importlib
# ---------------------------------------------------------------------------------------------------------------------------------------
class IuApi(object):

 # ---------------------------------------------------------------------------------------------------------------------------------------       
    @staticmethod
    def newEAction(action:str) -> EAction:
        try: 
            eAction = EAction()
            eAction.doGenerateID()
            eAction.doGenerateTime()
            eAction.action= action
            return eAction      
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise exception
        
    @staticmethod
    def addCApi(module:str):
        from evo_framework.core.evo_core_api.control.CApi import CApi
        
        if not module:
            raise Exception("ERROR_NONE_MODULE")
            
        arrayModule= module.split(".")
        className = arrayModule[-1]
        IuLog.doDebug(__name__, f"{module} {className}")
        ClassCApiAction = getattr(importlib.import_module(module), className)
        if ClassCApiAction:
            cApi=ClassCApiAction.getInstance()
            if isinstance(cApi,CApi):
                cApi.doAddApi()
            else:
                raise Exception("ERROR_IS_NOT_CAPI")         
        else:
            raise Exception("ERROR_NOT_VALID_MODULE_{module}")

# ---------------------------------------------------------------------------------------------------------------------------------------      
    @staticmethod
    def toData(enumApiType:EnumApiType, data, isUrl=False) ->bytes: 
       # IuLog.doVerbose(__name__,f"toDataApiType enumApiType:{enumApiType}") 

        if isinstance(data,bytes):
            return data

        if enumApiType == EnumApiType.STRING:
            return  IuBinary.toStrBytes(data)
        elif enumApiType == EnumApiType.LANGUAGE:
            return IuBinary.toStrBytes(data)
        elif enumApiType == EnumApiType.AUDIO:
            return IuBinary.toFileBytes(str(data))
        elif enumApiType == EnumApiType.VIDEO:
            return IuBinary.toFileBytes(str(data))
        elif enumApiType == EnumApiType.FILE:
            return IuBinary.toFileBytes(str(data))
        elif enumApiType == EnumApiType.IMAGE:
            return IuBinary.toFileBytes(str(data)) #TODO:check is PIL.IMAGE
        elif enumApiType == EnumApiType.INT:
            return IuBinary.toIntBytes(data)
        elif enumApiType == EnumApiType.FLOAT:
            return IuBinary.toFloatBytes(data)
        elif enumApiType == EnumApiType.DOUBLE:
            return IuBinary.toDoubleBytes(data)
        elif enumApiType == EnumApiType.BOOL:
            return IuBinary.toBoolBytes(data)
        elif enumApiType == EnumApiType.LONG:
            return IuBinary.toLongBytes(data)
        elif enumApiType == EnumApiType.EOBJECT:
            return data.toBytes()
        else:
            raise Exception(f"NOT_VALID_EnumApiType_{enumApiType}")

# ---------------------------------------------------------------------------------------------------------------------------------------   
    @staticmethod
    async def fromItem(enumApiType:EnumApiType, data:bytes, typeExt:str=None, ECLASS=None):
        IuLog.doVerbose(__name__,f"enumApiType:{enumApiType}")
        if enumApiType == EnumApiType.STRING:
            return IuBinary.fromStrBytes(data)
        elif enumApiType == EnumApiType.LANGUAGE:
            return IuBinary.fromStrBytes(data)
        elif enumApiType == EnumApiType.AUDIO:
            return await IuApi.toFile(enumApiType, data, typeExt)
        elif enumApiType == EnumApiType.VIDEO:
            return await IuApi.toFile(enumApiType, data, typeExt)
        elif enumApiType == EnumApiType.FILE:
            return await IuApi.toFile(enumApiType, data, typeExt)
        elif enumApiType == EnumApiType.IMAGE:
            return await IuApi.toFile(enumApiType, data, typeExt)
        elif enumApiType == EnumApiType.INT:
            return IuBinary.fromIntBytes(data)
        elif enumApiType == EnumApiType.FLOAT:
            return IuBinary.fromFloatBytes(data)
        elif enumApiType == EnumApiType.DOUBLE:
            return IuBinary.fromFloatBytes(data)
        elif enumApiType == EnumApiType.BOOL:
            return await IuBinary.fromBoolBytes(data)
        elif enumApiType == EnumApiType.LONG:
            return await IuBinary.fromLongBytes(data)
        elif enumApiType == EnumApiType.EOBJECT:
            if ECLASS is None :
                raise Exception("NOT_VALID_ECLASS")
            return IuApi.toEObject(ECLASS(), data)
        else:
            raise Exception(f"NOT_VALID_EnumApiType_{enumApiType}")
        
# ---------------------------------------------------------------------------------------------------------------------------------------           
    @staticmethod
    def toEObject(eObject:EObject, data: bytes) -> EObject :
        if data is None:
            raise Exception("ERROR_DATA_IS_NONE")
        return eObject.fromBytes(data)
# ---------------------------------------------------------------------------------------------------------------------------------------        
    @staticmethod
    def fromByteArray(pathFile:str, data:bytes) -> bytes:
        try:
            IuLog.doVerbose(__name__,f"pathFile: {pathFile}")
            if(pathFile is None):
                raise Exception("pathFile_null")
            dataOutput = None
            with open(pathFile, 'rb') as file:
                    dataOutput = file.read()
                 
            IuLog.doVerbose(__name__,f"pathFile len: {len(dataOutput)}")
            
            return dataOutput   
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise exception
# ---------------------------------------------------------------------------------------------------------------------------------------    
    @staticmethod
    async def toFile(enumApiType:EnumApiType, data:bytes, typeExt:str) -> str:
        try:    
            #@TODO: check mime type
            idFile = IuKey.generateId() 
            if(data is None):
                raise Exception("eApiType.dataInput_null")
            if(typeExt is None):
                raise Exception("eApiType.typeExt_null")
            
            if not typeExt.startswith(".") :
                typeExt = f".{typeExt}"
            directoryOutput = "/tmp/cyborgai"
            
            if not os.path.exists(directoryOutput):
                os.makedirs(directoryOutput)
            
            pathFile = f"{directoryOutput}/{idFile}{typeExt}"
            
            IuLog.doVerbose(__name__,f"pathFile: {idFile} {len(data)} {pathFile}")
            
            async with aiofiles.open(pathFile, mode='wb') as file:
                await file.write(data)
                await file.flush()     
                return pathFile

        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise exception
        
# ---------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def doLoadFile(pathFile, isJson=True):
        try:
            IuLog.doDebug(__name__,f"pathFile:{pathFile} isJson:{isJson}")
            with open(pathFile, 'r',encoding='utf-8') as fileData:
                if isJson:
                   return json.load(fileData) 
                else:
                    return fileData.read()   
            
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise exception  

       