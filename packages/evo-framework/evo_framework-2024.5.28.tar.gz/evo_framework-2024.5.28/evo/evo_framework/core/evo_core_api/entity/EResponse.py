from evo.evo_framework.entity.EObject import EObject
from evo.evo_framework.core.evo_core_api.entity.ERequest import ERequest

class EResponse(ERequest):
    def __init__(self):
        super().__init__()
        self.result = -1
        
    def toStream(self, stream):
        super().toStream(stream)
        self._doWriteInt(self.result, stream)

    def fromStream(self, stream):
        super().fromStream(stream)
        self.result = self._doReadInt(stream)
        
    def __str__(self) -> str:
        strReturn = "\n".join([
                            super().__str__(),
                            f"result:{self.result}",
                            ]) 
        return strReturn
        
