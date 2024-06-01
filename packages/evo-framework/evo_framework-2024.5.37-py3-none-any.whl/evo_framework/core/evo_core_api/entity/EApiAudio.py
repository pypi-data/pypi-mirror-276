#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EApiAudio

	this is EAPIAudio DESCRIPTION
	
"""
class EApiAudio(EObject):

	VERSION:str="3c37d0d7315664187980d10bc9abe5541b93f38ef107473e66bc336fac026f55"

	def __init__(self):
		super().__init__()
		
		self.isUrl:bool = None
		self.name:str = None
		self.ext:str = None
		self.length:int = None
		self.data:bytes = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteBool(self.isUrl, stream)
		self._doWriteStr(self.name, stream)
		self._doWriteStr(self.ext, stream)
		self._doWriteInt(self.length, stream)
		self._doWriteBytes(self.data, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.isUrl = self._doReadBool(stream)
		self.name = self._doReadStr(stream)
		self.ext = self._doReadStr(stream)
		self.length = self._doReadInt(stream)
		self.data = self._doReadBytes(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tisUrl:{ self.isUrl  }",
				f"\tname:{ self.name  }",
				f"\text:{ self.ext  }",
				f"\tlength:{ self.length  }",
				#f"\tdata:{ self.data  }",
							]) 
		return strReturn
	