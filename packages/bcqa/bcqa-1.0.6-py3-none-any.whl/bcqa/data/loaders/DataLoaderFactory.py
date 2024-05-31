from bcqa.config.constants import Dataset, Split
from bcqa.data.loaders.AmbigQADataLoader import AmbigQADataLoader
from bcqa.data.loaders.FinQADataLoader import FinQADataLoader
from bcqa.data.loaders.MusiqueQaDataLoader import MusiqueQADataLoader

from bcqa.data.loaders.OTTQADataLoader import OTTQADataLoader
from bcqa.data.loaders.TATQADataLoader import TATQADataLoader
from bcqa.data.loaders.WikiMultihopQADataLoader import WikiMultihopQADataLoader
from bcqa.data.loaders.StrategyQADataLoader import StrategyQADataLoader



class DataLoaderFactory:
    def __int__(self):
        pass

    def create_dataloader(
        self,
        dataloader_name: str,
        tokenizer="bert-base-uncased",
        config_path="test_config.ini",
        split=Split.TRAIN,
        batch_size=None,
        corpus=None
    ):
        if Dataset.AMBIGQA in dataloader_name:
            loader = AmbigQADataLoader
        elif Dataset.FINQA in dataloader_name:
            loader = FinQADataLoader
        elif Dataset.WIKIMULTIHOPQA in dataloader_name:
            loader = WikiMultihopQADataLoader
        elif Dataset.MUSIQUEQA in dataloader_name:
            loader = MusiqueQADataLoader
        elif Dataset.TATQA in dataloader_name:
            loader = TATQADataLoader  
        elif Dataset.OTTQA in dataloader_name:
            loader = OTTQADataLoader
        elif Dataset.StrategyQA in dataloader_name:
            loader = StrategyQADataLoader
        else:
            raise NotImplemented(f"{dataloader_name} not implemented yet.")
        return loader(dataset=dataloader_name, config_path=config_path,
                      split=split,batch_size=batch_size,
                      tokenizer=tokenizer,
                      corpus=corpus)