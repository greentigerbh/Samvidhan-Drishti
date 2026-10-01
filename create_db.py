import sqlite3
from pathlib import Path

BASE = Path.home() / "samvidhan_drishti"
DB = BASE / "database" / "archive.db"

DB.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)

conn.executescript("""
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    file_path TEXT NOT NULL UNIQUE,
    file_type TEXT,
    year INTEGER,
    language TEXT,
    source TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS debates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    date TEXT,
    file_path TEXT NOT NULL UNIQUE,
    source TEXT
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    media_type TEXT NOT NULL,
    file_path TEXT NOT NULL UNIQUE,
    source TEXT
);

CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    url TEXT,
    description TEXT
);

CREATE INDEX IF NOT EXISTS idx_documents_category
ON documents(category);

CREATE INDEX IF NOT EXISTS idx_debates_date
ON debates(date);

CREATE INDEX IF NOT EXISTS idx_media_type
ON media(media_type);
""")

# Official sources
sources = [
    (
        "Dr. Ambedkar Foundation",
        "https://www.drambedkarwritings.gov.in/",
        "Writings, speeches, audio, video and archival material"
    ),
    (
        "Constitution of India Digital Archive",
        "https://www.constitutionofindia.net/",
        "Constituent Assembly debates and constitutional material"
    )
]

for name, url, description in sources:
    conn.execute(
        "INSERT OR IGNORE INTO sources(name,url,description) VALUES(?,?,?)",
        (name, url, description)
    )

# -------------------------
# Writings / PDFs
# -------------------------
writing_dir = BASE / "writings"

if writing_dir.exists():
    for f in writing_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() == ".pdf":
            title = f.stem.replace("_", " ")

            conn.execute("""
                INSERT OR IGNORE INTO documents
                (title, category, file_path, file_type, source)
                VALUES (?, ?, ?, ?, ?)
            """, (
                title,
                "Writings",
                str(f),
                "PDF",
                "Dr. Ambedkar Foundation"
            ))

# -------------------------
# Debates
# -------------------------
debate_dir = BASE / "debates"

if debate_dir.exists():
    for f in debate_dir.rglob("*.html"):
        title = f.stem.replace("-", " ").title()

        conn.execute("""
            INSERT OR IGNORE INTO debates
            (title, file_path, source)
            VALUES (?, ?, ?)
        """, (
            title,
            str(f),
            "Constitution of India Digital Archive"
        ))

# -------------------------
# Audio
# -------------------------
audio_dir = BASE / "audio"

if audio_dir.exists():
    for f in audio_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() in [
            ".mp3", ".wav", ".ogg", ".m4a", ".aac"
        ]:
            conn.execute("""
                INSERT OR IGNORE INTO media
                (title, media_type, file_path, source)
                VALUES (?, ?, ?, ?)
            """, (
                f.stem.replace("_", " "),
                "Audio",
                str(f),
                "Dr. Ambedkar Foundation"
            ))

# -------------------------
# Video
# -------------------------
video_dir = BASE / "video"

if video_dir.exists():
    for f in video_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() in [
            ".mp4", ".mkv", ".avi", ".mov", ".webm"
        ]:
            conn.execute("""
                INSERT OR IGNORE INTO media
                (title, media_type, file_path, source)
                VALUES (?, ?, ?, ?)
            """, (
                f.stem.replace("_", " "),
                "Video",
                str(f),
                "Dr. Ambedkar Foundation"
            ))

# -------------------------
# Images
# -------------------------
image_dir = BASE / "images"

if image_dir.exists():
    for f in image_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() in [
            ".jpg", ".jpeg", ".png", ".webp", ".gif"
        ]:
            conn.execute("""
                INSERT OR IGNORE INTO media
                (title, media_type, file_path, source)
                VALUES (?, ?, ?, ?)
            """, (
                f.stem.replace("_", " "),
                "Image",
                str(f),
                "Dr. Ambedkar Foundation"
            ))

conn.commit()

print("Database created successfully!")
print(f"Location: {DB}")

# Statistics
for table in ["documents", "debates", "media", "sources"]:
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]
    print(f"{table}: {count}")

conn.close()
