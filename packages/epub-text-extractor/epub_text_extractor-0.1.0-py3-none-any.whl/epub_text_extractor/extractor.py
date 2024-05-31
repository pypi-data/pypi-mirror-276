# extractor.py
from bs4 import BeautifulSoup

class EpubExtractor:
    def __init__(self, epub_items):
        self.epub_items = epub_items
        self.chapters = self._extract_chapters()

    def _extract_chapters(self):
        chapters = []
        for item in self.epub_items:
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text = soup.get_text()
            chapters.append({
                'title': item.get_name(),
                'content': text
            })
        return chapters

    def get_content_as_text(self):
        return '\n\n'.join([chapter['content'] for chapter in self.chapters])

    def get_content_as_json(self):
        import json
        return json.dumps(self.chapters, indent=4, ensure_ascii=False)
