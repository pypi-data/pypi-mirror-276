#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap
from evo_framework.core.evo_core_api.entity.EnumApiAction import EnumApiAction
#========================================================================================================================================
"""EAction

	this is EAction DESCRIPTION
	
"""
class EAction(EObject):

	VERSION:str="2fb34e332b25762d5c8b1a9c054b537e46aa53785799f595a4c1c0a0d5d769fb"

	def __init__(self):
		super().__init__()
		self.enumApiAction:EnumApiAction = EnumApiAction.NONE
		self.action:str = None
		self.input:bytes = None
		self.output:bytes = None
  
	def toStream(self, stream):
		super().toStream(stream)
		self._doWriteInt(self.enumApiAction.value, stream)
		self._doWriteStr(self.action, stream)
		self._doWriteBytes(self.input, stream)
		self._doWriteBytes(self.output, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)	
		self.enumApiAction = EnumApiAction(self._doReadInt(stream))
		self.action = self._doReadStr(stream)
		self.input = self._doReadBytes(stream)
		self.output = self._doReadBytes(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),			
				f"\tenumApiAction:{ self.enumApiAction  }",
				f"\taction:{ self.action  }",
				f"\tinput len: {len(self.input) if self.input else 'None'}",
            	f"\toutput len: {len(self.output) if self.output else 'None'}"
							]) 
		return strReturn
	