#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EResponse

	
	
"""
class EResponse(EObject):

	VERSION:str="54783dcdbebf95b048867fba76128db1939e123403ea6f64633ec42c83154ca1"

	def __init__(self):
		super().__init__()
		
		self.sign:bytes = None
		self.hash:bytes = None
		self.chunk:int = None
		self.chunkTotal:int = None
		self.length:int = None
		self.data:bytes = None
		self.isError:bool = None
		self.error:str = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteBytes(self.sign, stream)
		self._doWriteBytes(self.hash, stream)
		self._doWriteInt(self.chunk, stream)
		self._doWriteInt(self.chunkTotal, stream)
		self._doWriteInt(self.length, stream)
		self._doWriteBytes(self.data, stream)
		self._doWriteBool(self.isError, stream)
		self._doWriteStr(self.error, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.sign = self._doReadBytes(stream)
		self.hash = self._doReadBytes(stream)
		self.chunk = self._doReadInt(stream)
		self.chunkTotal = self._doReadInt(stream)
		self.length = self._doReadInt(stream)
		self.data = self._doReadBytes(stream)
		self.isError = self._doReadBool(stream)
		self.error = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tsign:{self.sign!r}",
				f"\thash:{self.hash!r}",
				f"\tchunk:{self.chunk}",
				f"\tchunkTotal:{self.chunkTotal}",
				f"\tlength:{self.length}",
				#f"\tdata:{ self.data  }",
				f"\tisError:{self.isError}",
				f"\terror:{self.error}",
							]) 
		return strReturn
	