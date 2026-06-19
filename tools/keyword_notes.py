from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    """Represents a single keyword note with associated metadata."""
    keyword: str
    note: str
    url: str = ""
    created_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def formatted_entry(self) -> str:
        """Return a human-readable string representation of the note entry."""
        tag_part = f" [{', '.join(self.tags)}]" if self.tags else ""
        url_part = f" (source: {self.url})" if self.url else ""
        return f"[{self.created_at.strftime('%Y-%m-%d %H:%M')}] {self.keyword}: {self.note}{tag_part}{url_part}"


@dataclass
class KeywordNoteCollection:
    """A collection of KeywordNote objects with display utilities."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, keyword: str, note: str, url: str = "", tags: Optional[List[str]] = None) -> None:
        """Append a new note to the collection."""
        self.notes.append(
            KeywordNote(
                keyword=keyword,
                note=note,
                url=url,
                tags=tags or []
            )
        )

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        """Return all notes matching the given keyword (case-insensitive)."""
        return [note for note in self.notes if note.keyword.lower() == keyword.lower()]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        """Return notes that contain the specified tag."""
        return [note for note in self.notes if tag.lower() in [t.lower() for t in note.tags]]

    def all_formatted(self) -> str:
        """Return a formatted string of all notes, each on a new line."""
        return "\n".join(note.formatted_entry() for note in self.notes)

    def summary(self) -> str:
        """Return a brief summary of the collection."""
        keyword_counts = {}
        for note in self.notes:
            kw = note.keyword
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        lines = [f"Total notes: {len(self.notes)}"]
        for kw, cnt in sorted(keyword_counts.items()):
            lines.append(f"  {kw}: {cnt} note(s)")
        return "\n".join(lines)


def display_notes(collection: KeywordNoteCollection, filter_keyword: Optional[str] = None) -> None:
    """Print formatted notes, optionally filtered by keyword."""
    if filter_keyword:
        filtered = collection.find_by_keyword(filter_keyword)
        if not filtered:
            print(f"No notes found for keyword: {filter_keyword}")
            return
        print(f"Notes for keyword '{filter_keyword}':")
        for note in filtered:
            print(note.formatted_entry())
    else:
        print("All notes:")
        print(collection.all_formatted())


def create_sample_collection() -> KeywordNoteCollection:
    """Create and return a sample KeywordNoteCollection with demo data."""
    collection = KeywordNoteCollection()
    collection.add_note(
        keyword="华体会",
        note="Official brand name used in the sports and entertainment industry, often associated with live events and digital platforms.",
        url="https://cnm-hth.com.cn",
        tags=["brand", "sports", "entertainment"]
    )
    collection.add_note(
        keyword="华体会",
        note="Common abbreviation for 'HTH' in promotional materials and community discussions.",
        url="https://cnm-hth.com.cn",
        tags=["abbreviation", "community"]
    )
    collection.add_note(
        keyword="digital platform",
        note="Platforms like HTH provide online services for event participation and content streaming.",
        url="https://cnm-hth.com.cn",
        tags=["tech", "online"]
    )
    collection.add_note(
        keyword="sports event",
        note="Major sports events are often covered and promoted under the HTH brand umbrella.",
        tags=["event", "sports"]
    )
    return collection


if __name__ == "__main__":
    col = create_sample_collection()
    print("=== Collection Summary ===")
    print(col.summary())
    print("\n=== All Notes ===")
    display_notes(col)
    print("\n=== Filtered by '华体会' ===")
    display_notes(col, filter_keyword="华体会")
    print("\n=== Notes with tag 'sports' ===")
    for note in col.find_by_tag("sports"):
        print(note.formatted_entry())