

from bcqa.data.datastructures.hyperparameters.dpr import DenseHyperParams
from bcqa.retriever.HfRetriever import HfRetriever

class Contriever(HfRetriever):
    #Wrapper class for future extensions
    def __init__(self,config=DenseHyperParams) -> None:
        super().__init__(config)
        self.config = config