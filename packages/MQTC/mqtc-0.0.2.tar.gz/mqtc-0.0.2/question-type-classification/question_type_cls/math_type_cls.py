from question_type_cls.inference.predict import Classifier
from question_type_cls.inference.rulebased import rulebase_cls
from typing import List, Union

import torch

def math_type_cls(texts: Union[str, List[str]], model_type='model-based'):
    if model_type == 'model-based':
        path = 'question-type-classification/question_type_cls/2305-output'
        device_map = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        classifier = Classifier(model_name_or_path=path, device_map=device_map, max_length=256)
        predictions = classifier(texts)
        return predictions
    if model_type == 'rule-based':
        if isinstance(texts, str):
            predictions = [{'label': rulebase_cls(texts)}]
        else:
            predictions = list(map(lambda text: rulebase_cls(text), texts))
        return predictions
    else:
        print ('Please choose a model type: model-based or rule-based!')
        predictions = None
    return predictions

