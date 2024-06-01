from flexidata.parser.document import DocumentParser
from flexidata.utils.constants import FileType, FileReaderSource


parser = DocumentParser(
    file_type=FileType.MD,
    file_path="/app/flexi-data/example-docs/markdown.md",
    source=FileReaderSource.LOCAL,
)
text_blocks = parser.parse()
for text_block in text_blocks:
    print(text_block)
