from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator
from uuid import uuid4
from pathlib import Path

class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    path: Optional[str] = None
    data: Any = None
    metadata: Dict[str, Any] = {}
    parents: List[str] = []
    childrens: List[str] = []

    @field_validator('path')
    def check_path_exists(cls, value):
        if value:
            path = Path(value)
            if not path.exists():
                raise ValueError(f"El archivo en la ruta '{value}' no existe.")
            return value

    def read(self):
        """
        Método personalizado para leer el archivo. Define self.data,
        """
        if self.path:
            try:
                with open(self.path, 'rb') as file:
                    self.data = file.read()
                    return self
            except Exception as e:
                print(f"Error al leer el archivo: {e}")
                raise e

        raise FileNotFoundError("Defina la ruta del archivo")

    def save(self, path: str):
        self.path = path
        _path = Path(path)
        folder = _path.parent
        folder.mkdir(parents=True, exist_ok=True)
        return self.saver(path)

    def saver(self, path):
        """ Clase personalizada para almacenar los datos """
        with open(path, 'wb') as file:
            file.write(self.data)
        return self

    def append(self, parent: 'Document'):
        # Si se agrega un documento adicional, este será padre
        self.parents.append(parent.id)

        # Y debemos agregar a este como hijo
        parent.childrens.append(self.id)
        return self.appender(parent)

    def appender(self, parent):
        """Clase que puede sobreescribirse con la lógica personalizada"""
        return self

    def extend(self, parents: List['Document']):
        # Si se agregan documentos adicionales, estos serán padres
        self.parents.extend([parent.id for parent in parents])

        # Y debemos agregarlo como hijo
        [parent.childrens.append(self.id) for parent in parents]
        return self.extender(parents)

    def extender(self, others):
        """Agrega los contenidos de otros documentos markdown"""
        for other in others:
            self.appender(other)
        return self