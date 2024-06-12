import pytest
from models.author import Author
from models.article import Article  
from models.magazine import Magazine
from database.connection import get_db_connection

# Helper functions
def drop_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS articles")
    cursor.execute("DROP TABLE IF EXISTS authors")
    cursor.execute("DROP TABLE IF EXISTS magazines")
    conn.commit()
    cursor.close()
    conn.close()

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE magazines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors (id),
            FOREIGN KEY (magazine_id) REFERENCES magazines (id)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Fixture to create tables before each test
@pytest.fixture(autouse=True)
def setup_database():
    drop_tables()
    create_tables()

@pytest.fixture
def author():
    return Author(name='Mary Ann')

@pytest.fixture
def magazine():
    return Magazine(name='Example Magazine', category='Fashion')

def test_article_creation(author, magazine):
    article = Article(author, magazine, "Test Title", "Test Content")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = ?", (article.id,))
    article_from_db = cursor.fetchone()
    cursor.close()
    conn.close()

    assert article_from_db is not None
    assert article_from_db[1] == "Test Title"
    assert article_from_db[2] == "Test Content"
    assert article_from_db[3] == author.id
    assert article_from_db[4] == magazine.id

def test_get_author(author, magazine):
    article = Article(author, magazine, "Test Title", "Test Content")
    author_name = article.get_Author()
    assert author_name == author.name

def test_get_magazine(author, magazine):
    article = Article(author, magazine, "Test Title", "Test Content")
    magazine_name = article.get_magazine()
    assert magazine_name == magazine.name

def test_article_title_validation(author, magazine):
    valid_article = Article(author, magazine, "Valid Title", "Test Content")
    assert valid_article.title == "Valid Title"
