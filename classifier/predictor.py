import pickle
import random
from pathlib import Path
from typing import Dict, Any, Union, Optional


class Predictor:


    def __init__(self, load_path: Optional[Union[str, Path]]=None):
        pass

    def predict(self, input: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplemented(f".predict() not implemented for {self}")


class SklearnPredictor(Predictor):
    
    def __init__(self, load_path: Union[str, Path]):
        pass

    def predict(self, input: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplemented(f".predict() not implemented for {self}")


class CatboostPredictor(Predictor):
    pass


class BertPredictor(Predictor):
    
    def __init__(self, load_path: Union[str, Path]):
        pass

    def predict(self, input: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplemented(f".predict() not implemented for {self}")


class RandomPredictor(Predictor):

    def predict(self, input: Dict[str, Any]) -> Dict[str, Any]:
        p = random.random()
        return {"prob": p, "class": int(p > 0.5)}


def get_predictor(predictor_type: str, load_path: Optional[Union[str, Path]] = None) -> Predictor:
    predictor_mapping = {"random": RandomPredictor, "bert": BertPredictor, "sklearn": SklearnPredictor}
    predictor_class = predictor_mapping[predictor_type]
    return predictor_class(load_path=load_path)
