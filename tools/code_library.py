import json
from pathlib import Path

class CodeLibrary:
    """Manage a local shared code snippet library"""
    def __init__(self, filepath=None):
        # Default storage in workspace root
        default = Path(__file__).parent.parent / 'code_snippets.json'
        self.filepath = Path(filepath) if filepath else default
        self.snippets = []
        self.load()

    def load(self):
        if self.filepath.exists():
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.snippets = json.load(f)
            except Exception:
                self.snippets = []
        else:
            self.snippets = []

    def save(self):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.snippets, f, indent=2)
        except Exception as e:
            print(f"Error saving code library: {e}")

    def add_snippet(self, title, code, tags=None):
        """Add a new snippet with title, code, and optional tags"""
        tags = tags or []
        snippet = {
            'id': len(self.snippets) + 1,
            'title': title,
            'code': code,
            'tags': tags
        }
        self.snippets.append(snippet)
        self.save()
        return snippet

    def list_snippets(self):
        """Return all snippets"""
        return self.snippets

    def search_by_tag(self, tag):
        """Return snippets matching a tag"""
        return [s for s in self.snippets if tag in s.get('tags', [])]

    def search_by_keyword(self, keyword):
        """Return snippets matching keyword in title or code"""
        key = keyword.lower()
        return [s for s in self.snippets if key in s['title'].lower() or key in s['code'].lower()]
