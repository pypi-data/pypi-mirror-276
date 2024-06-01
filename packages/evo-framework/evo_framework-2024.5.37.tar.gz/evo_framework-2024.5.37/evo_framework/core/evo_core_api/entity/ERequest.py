#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EnumApiCrypto import EnumApiCrypto
#========================================================================================================================================
"""ERequest

	
	
"""
class ERequest(EObject):

	VERSION:str="7f435f4aa8b838214b2b13090fe503295d209568f9d85087ecd86877bcf9ae74"

	def __init__(self):
		super().__init__()
		
		self.enumApiCrypto:EnumApiCrypto = EnumApiCrypto.ECC
		self.pk:bytes = None
		self.cipher:bytes = None
		self.sign:bytes = None
		self.hash:bytes = None
		self.chunk:int = None
		self.chunkTotal:int = None
		self.length:int = None
		self.data:bytes = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteInt(self.enumApiCrypto.value, stream)
		self._doWriteBytes(self.pk, stream)
		self._doWriteBytes(self.cipher, stream)
		self._doWriteBytes(self.sign, stream)
		self._doWriteBytes(self.hash, stream)
		self._doWriteInt(self.chunk, stream)
		self._doWriteInt(self.chunkTotal, stream)
		self._doWriteInt(self.length, stream)
		self._doWriteBytes(self.data, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.enumApiCrypto = EnumApiCrypto(self._doReadInt(stream))
		self.pk = self._doReadBytes(stream)
		self.cipher = self._doReadBytes(stream)
		self.sign = self._doReadBytes(stream)
		self.hash = self._doReadBytes(stream)
		self.chunk = self._doReadInt(stream)
		self.chunkTotal = self._doReadInt(stream)
		self.length = self._doReadInt(stream)
		self.data = self._doReadBytes(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tenumApiCrypto:{self.enumApiCrypto}",
				f"\tpk:{self.pk!r}",
				f"\tcipher:{self.cipher!r}",
				f"\tsign:{self.sign!r}",
				f"\thash:{self.hash!r}",
				f"\tchunk:{self.chunk}",
				f"\tchunkTotal:{self.chunkTotal}",
				f"\tlength:{self.length}",
				#f"\tdata:{ self.data  }",
							]) 
		return strReturn
	