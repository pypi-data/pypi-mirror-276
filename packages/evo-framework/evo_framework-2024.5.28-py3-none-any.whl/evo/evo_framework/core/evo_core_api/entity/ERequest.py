
from evo.evo_framework.entity.EObject import EObject
from evo.evo_framework.core.evo_core_api.entity.EnumApiCrypto import EnumApiCrypto

class ERequest(EObject):
    def __init__(self):
        super().__init__()
        self.enumCrypto:EnumApiCrypto = EnumApiCrypto.NONE
        self.pk: bytes = None
        self.cipher: bytes = None
        self.sign: bytes = None
        self.hash: bytes = None
        self.chunk: int = 1  
        self.chunkTotal: int = 1  
        self.length: int = -1  
        self.data: bytes = None

    def toStream(self, stream):
        super().toStream(stream)
        self._doWriteInt(self.enumCrypto.value, stream)
        self._doWriteBytes(self.pk, stream)
        self._doWriteBytes(self.cipher, stream)
        self._doWriteBytes(self.sign, stream)
        self._doWriteBytes(self.hash, stream)
        self._doWriteInt(self.chunk, stream)
        self._doWriteInt(self.chunkTotal, stream)
        self._doWriteLong(self.length, stream)
        self._doWriteBytes(self.data, stream)

    def fromStream(self, stream):
        super().fromStream(stream)
        self.enumCrypto = EnumApiCrypto(self._doReadInt(stream))
        self.pk = self._doReadBytes(stream)
        self.cipher = self._doReadBytes(stream)
        self.sign = self._doReadBytes(stream)
        self.hash = self._doReadBytes(stream)
        self.chunk = self._doReadInt(stream)
        self.chunkTotal = self._doReadInt(stream)
        self.length = self._doReadLong(stream)
        self.data = self._doReadBytes(stream)
        
    def __str__(self) -> str:
        strReturn = "\n".join([
                            super().__str__(),
                            f"enumCrypto:{self.enumCrypto}",
                            f"pk:{self.pk!r}",
                            f"cipher:{self.cipher!r}",
                            f"sign:{self.sign!r}",
                            f"hash:{self.hash!r}",
                            f"chunk:{self.chunk}",
                            f"chunkTotal:{self.chunkTotal}",
                            f"length:{self.length}",
                            ]) 
        return strReturn
