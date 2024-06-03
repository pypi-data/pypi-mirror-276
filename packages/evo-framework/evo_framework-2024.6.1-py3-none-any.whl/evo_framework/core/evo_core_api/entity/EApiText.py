#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EApiText

	EApiFile DESCRIPTION
	
"""
class EApiText(EObject):

	VERSION:str="4672b9fb466a618ab6adfeb34e328702670ec6af44d6d64619bb99b3d132fcfe"

	def __init__(self):
		super().__init__()
		self.language:str = "en-US"
		self.text:str = None
		self.isComplete:bool = None
  
	def toStream(self, stream):
		super().toStream(stream)
		self._doWriteStr(self.language, stream)
		self._doWriteStr(self.text, stream)
		self._doWriteBool(self.isComplete, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		self.language = self._doReadStr(stream)
		self.text = self._doReadStr(stream)
		self.isComplete = self._doReadBool(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),			
				f"\tlanguage:{self.language}",
				f"\ttext:{self.text}",
				f"\tisComplete:{self.isComplete}",
							]) 
		return strReturn
	