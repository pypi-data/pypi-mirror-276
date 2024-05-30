from loguru import logger


def map_label2id(label: str, label2id: dict) -> int:
    """Mapping label (text) to id"""
    return label2id[label]


def print_trainable_parameters(model):
    """
    Prints the number of trainable parameters in the model.
    """
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    logger.info(
        f"Trainable params: {trainable_params} || All params: {all_param} || Trainable: {100 * trainable_params / all_param}%"
    )
