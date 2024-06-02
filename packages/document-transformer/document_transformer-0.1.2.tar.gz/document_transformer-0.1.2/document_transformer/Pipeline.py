from typing import List, Union, Any
from pydantic import BaseModel
from .Document import Document
from .Transformer import DocumentTransformer

from typing import get_type_hints, get_origin

class Pipeline(BaseModel):

    transformers: List[DocumentTransformer]
    all_docs: Any = []

    def run(self, input: Union[Document, List[Document]]) -> Union[Document, List[Document]]:
        output = input

        # Incializamos all_docs, que llevará la traza de todos los documentos
        self.all_docs.extend(self.process_result(output))

        for transformer in self.transformers:

            if isinstance(output, list):
                input_types = get_type_hints(transformer)['input']

                if get_origin(input_types) == list:
                    # Si input está declarado como una lista, aplicar la transformación a todos los documentos
                    transformer.input = output
                    output = transformer.run()

                else:
                    # Sino, aplicar la transformación a cada documento
                    transformed_docs = []
                    for out in output:
                        transformer.input = out
                        result = transformer.run()
                        transformed_docs.extend(self.process_result(result))
                    output = transformed_docs
            else:
                # Si output es documento, aplicar la transformación directamente
                transformer.input = output
                output = transformer.run()

            self.all_docs.extend(self.process_result(output))

        return output

    def process_result(self, result):
        if isinstance(result, list):
            return result
        return [result]

    def get_traces(self):
        return [
            {
                "id": doc.id,
                "path": doc.path,
                "type": type(doc).__name__,
                "childrens": [child for child in doc.childrens],
                "parents": [parent for parent in doc.parents],
            }
            for doc in self.all_docs
        ]