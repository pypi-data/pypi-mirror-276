from markdownfeedgenerator.Generators.Default.Models import ItemStore
from markdownfeedgenerator.MarkdownFile import MarkdownFile


class FeedItem:
    def __init__(
        self
    ):
        self.store = ItemStore()
        self.markdown_file: MarkdownFile | None = None

    def inject_markdown_file(
        self,
        markdown_file: MarkdownFile
    ):
        self.markdown_file = markdown_file
        self.store.inject(markdown_file.front_matter)

    def inject_dict(
        self,
        injectable: dict
    ):
        self.store.inject(injectable)

    def get(
        self,
        key: str
    ) -> any:
        return self.store.get(key)

    def has(
        self,
        key: str
    ) -> any:
        return self.store.has(key)

    def has_value(
        self,
        key: str
    ) -> bool:
        return self.store.has_value(key)

    def set(
        self,
        key: str,
        data: any
    ) -> any:
        return self.store.set(key, data)

    def dump(
        self
    ) -> dict:
        return self.store.dump()

    def check(
        self
    ):
        self.store.check()

    def __str__(self):
        if self.markdown_file:
            return str(self.markdown_file)

        return super().__str__()
