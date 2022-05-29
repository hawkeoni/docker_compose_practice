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
        self.pipeline = pickle.load(open(load_path, "rb"))

    def predict(self, input: Dict[str, Any]) -> Dict[str, Any]:
        prob = self.pipeline.predict_proba([input["text"]])[0][1]
        return {"prob": prob, "class": int(prob > 0.5)}


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
