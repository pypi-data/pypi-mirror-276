from question_type_cls.inference.predict import Classifier
import torch

def math_type(text):
    path = 'question-type-classification/question_type_cls/2305-output'
    device_map = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    classifier = Classifier(model_name_or_path=path, device_map=device_map, max_length=256)
    predictions = classifier(text)
    return predictions

# text = '1+1'
# print (math_type(text))


