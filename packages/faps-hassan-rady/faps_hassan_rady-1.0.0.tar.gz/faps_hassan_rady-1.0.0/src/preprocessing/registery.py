from preprocessing.base import PreProcessor

_pre_processor_registry: dict[str, PreProcessor] = {}


def add_pre_processor_to_registry(pre_processor: PreProcessor) -> None:
    _pre_processor_registry[pre_processor.name] = pre_processor


def get_pre_processor_from_registry(name: str) -> PreProcessor:
    return _pre_processor_registry[name]
