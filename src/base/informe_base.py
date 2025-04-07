# src/base/informe_base.py
import abc

class InformeBase(abc.ABC):
    def __init__(self, path_txt, root_dir):
        self.path_txt = path_txt
        self.root_dir = root_dir

    @abc.abstractmethod
    def procesar(self):
        pass