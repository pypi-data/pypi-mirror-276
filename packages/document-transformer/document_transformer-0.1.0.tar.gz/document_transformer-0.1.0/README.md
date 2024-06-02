# Document Transformer

Document Transformer allows users to define and apply transformations to documents in a flexible and robust manner, ensuring traceability of each change made to the documents.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- Flexible document transformation
- Comprehensive traceability for each transformation
- Add custom supports to multiple document formats (e.g., JSON, XML, CSV)
- Easy integration with other tools and workflows

## Installation

To install Document Transformer, follow these steps:

```sh
# Install using pip
pip install document-transformer
```

## Usage

Define custom Document class

```python
from document_transformer import Document

class PDFDocument(Document):
    """Custom class to PDF Documents"""

class ImageDocument(Document):
    """Custom class to Image Documents"""
    def saver(self, path):
        self.data.save(path)
        return self
```

Define the transformer. Specify input and output Document types

```python
from document_transformer import DocumentTransformer
import pdf2image  # install: pip install pdf2image
from typing import List
from pathlib import Path

class PDF2Images(DocumentTransformer):
    input: PDFDocument = None
    output: List[ImageDocument] = []

    def transformer(self) -> List[ImageDocument]:
        """Split the PDF document into pages"""
        images = pdf2image.convert_from_path(self.input.path)
        return [
            ImageDocument(
                metadata={'pdf_path': Path(self.input.path).name, 'page': i+1, 'size': image.size},
                data=image,
            )
            for i, image in enumerate(images)
        ]
```

Run your implementation

```python
pdf_doc = PDFDocument(path="document.pdf")
images = PDF2Images(input=pdf_doc).run()

for image in images:
    image.save(path=f'images/pag_{image.metadata["page"]}.jpg')
    print(f"Imagen: {image.id}")
    print(f"Parents: {image.parents}")
    print(f"Metadata: {image.metadata}")
```

Or run like a pipeline, visualize the graph transformation

```python
from document_transformer import Pipeline, plot_graph

# Define Pipeline, add more transformers as you need
pipeline = Pipeline(transformers=[
    PDF2Images(to="images/pag_{metadata[page]}.jpg"),
    # Images2Markdown(to="images/pag_{metadata[page]}.md")),
    # ...
])

# Define input and get output
pdf_doc = PDFDocument(path="document.pdf")
images = pipeline.run(input=pdf_doc)

# See transfomer plot graph
plot_graph(pipeline.get_traces())
```

![plot_graph.png](docs/static/plot_graph.png)

## Contributing
We welcome contributions! Please read our Contributing Guide to learn how you can help.

## License
Document Transformer is licensed under the MIT License

## Contact
If you have any questions or feedback, please feel free to reach out to us at johngonzalezv@gmail.com.
