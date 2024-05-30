from markdownfeedgenerator.Generators.Default.Models import ItemStore
from markdownfeedgenerator.MarkdownFile import MarkdownFile


class FeedItem(ItemStore):
    def __init__(
        self
    ):
        ItemStore.__init__(self)
        self.markdown_file: MarkdownFile | None = None

    def inject_markdown_file(
        self,
        markdown_file: MarkdownFile
    ):
        self.markdown_file = markdown_file
        self.inject(markdown_file.front_matter)

    def __str__(self):
        if self.markdown_file:
            return self.markdown_file.file_path

        return str(self.store)
