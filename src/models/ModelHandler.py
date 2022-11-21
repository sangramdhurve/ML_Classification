from types import ModuleType
from inspect import getmembers, isclass

try:
    from LogisticRegressionModel import LogisticRegressionModel
except ModuleNotFoundError:
    from .LogisticRegressionModel import LogisticRegressionModel

__all__ = ["LogisticRegressionModel", "ModelController"]


class ModelController:
    def __init__(self, model_name: str, logger=None):
        self.__logger = logger
        self.__model_name = model_name

    def get_model(self):
        obj = globals()[self.__model_name]
        if callable(obj):
            obj = obj(logger=self.__logger)
            return obj

        if isinstance(obj, ModuleType):
            all_classes = getmembers(obj, isclass)
            for class_tuple in all_classes:
                class_name = class_tuple[0]
                class_obj = class_tuple[1]

                if class_name == self.__model_name:
                    obj = class_obj(logger=self.__logger)
                    break
        return obj


if __name__ == '__main__':
    model_name = "LogisticRegressionModel"
    model_controller = ModelController(model_name=model_name)
    print(model_controller.get_model())