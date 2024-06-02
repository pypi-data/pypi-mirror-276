from abc import ABC, abstractmethod
from typing import List, Optional, Union
from pydantic import BaseModel
from pathlib import Path
from .Document import Document

class DocumentTransformer(ABC, BaseModel):
    input: Optional[Union[Document, List[Document]]] = None
    output: Optional[Union[Document, List[Document]]] = None
    to: Optional[Union[str, Path]] = None

    @abstractmethod
    def transformer(self) -> List[Document]:
        pass

    def get_save_path(self, document: Document, index: int = 0) -> Optional[Path]:
        if self.to:
            path = Path(self.to)
            if "{" in path.name and "}" in path.name:
                try:
                    doc_dict = document.dict()
                    formatted_path = str(path).format(**doc_dict)
                    return Path(formatted_path)
                except KeyError:
                    return path.parent / path.name.format(i=index)
            else:
                return path
        return None

    def run(self):
        self.output = self.transformer()

        # Verificar si output es una lista o un único documento
        if isinstance(self.output, list):
            # Muchos a muchos
            if isinstance(self.input, list):
                for i, output in enumerate(self.output):
                    output.parents = [input.id for input in self.input]
                    if save_path:=self.get_save_path(output, i):
                        output.save(str(save_path))  # Guardar documento
                for input in self.input:
                    input.childrens = [output.id for output in self.output]

            else:
                # uno a muchos
                for i, output in enumerate(self.output):
                    output.parents = [self.input.id]
                    if save_path:=self.get_save_path(output, i):
                        output.save(str(save_path))  # Guardar documento

                self.input.childrens = [output.id for output in self.output]

        else:
            # Si input es una lista (Muchos a uno)
            if isinstance(self.input, list):
                self.output.parents = [input.id for input in self.input]
                if save_path:=self.get_save_path(self.output):
                    self.output.save(str(save_path))  # Guardar documento

                for input in self.input:
                    input.childrens = [self.output.id]
            # sino: Agregar información de los padres a output (uno a uno)
            else:
                self.output.parents = [self.input.id]
                if save_path:=self.get_save_path(self.output):
                    self.output.save(str(save_path))
                self.input.childrens = [self.output.id]

        return self.output
