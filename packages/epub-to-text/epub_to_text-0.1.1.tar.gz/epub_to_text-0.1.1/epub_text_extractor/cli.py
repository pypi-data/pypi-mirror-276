# cli.py
import argparse
import os
from epub_text_extractor.reader import EpubReader
from epub_text_extractor.extractor import EpubExtractor
from epub_text_extractor.converter import ContentConverter

class EpubContentFeedAI:
    def __init__(self, epub_file_path, output_dir=None):
        self.epub_file_path = epub_file_path
        self.output_dir = output_dir or self._create_default_output_dir()
        self.reader = EpubReader(epub_file_path)
        self.book_title = self._sanitize_filename(self.reader.book.get_metadata('DC', 'title')[0][0])
        self.epub_items = self.reader.get_items()
        self.extractor = EpubExtractor(self.epub_items)

    def _create_default_output_dir(self):
        base_dir = os.path.dirname(self.epub_file_path)
        output_dir = os.path.join(base_dir, 'export')
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    @staticmethod
    def _sanitize_filename(name):
        import re
        return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

    def save_content_as_text(self):
        content_text = self.extractor.get_content_as_text()
        output_file = os.path.join(self.output_dir, f"{self.book_title}.txt")
        ContentConverter.save_as_text(content_text, output_file)
        print(f"Content saved as text in {output_file}")

    def save_content_as_json(self):
        content_json = self.extractor.get_content_as_json()
        output_file = os.path.join(self.output_dir, f"{self.book_title}.json")
        ContentConverter.save_as_json(content_json, output_file)
        print(f"Content saved as JSON in {output_file}")

    def save_content_as_markdown(self):
        content_text = self.extractor.get_content_as_text()
        content_markdown = ContentConverter.convert_to_markdown(content_text)
        output_file = os.path.join(self.output_dir, f"{self.book_title}.md")
        ContentConverter.save_as_text(content_markdown, output_file)
        print(f"Content saved as Markdown in {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Extract content from an EPUB file and export it in various formats.")
    parser.add_argument("epub_file", help="Path to the EPUB file")
    parser.add_argument("-o", "--output_dir", help="Directory to save the output files", default=None)
    parser.add_argument("--text", help="Export content as text", action="store_true")
    parser.add_argument("--json", help="Export content as JSON", action="store_true")
    parser.add_argument("--markdown", help="Export content as Markdown", action="store_true")

    args = parser.parse_args()

    if not os.path.isfile(args.epub_file):
        print(f"Error: EPUB file '{args.epub_file}' does not exist.")
        return

    content_feed_ai = EpubContentFeedAI(args.epub_file, args.output_dir)

    if args.text:
        content_feed_ai.save_content_as_text()
    if args.json:
        content_feed_ai.save_content_as_json()
    if args.markdown:
        content_feed_ai.save_content_as_markdown()

if __name__ == "__main__":
    main()
