from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, author, magazine, title, content):
        # Ensure the author and magazine are of the correct type
        if not isinstance(author, Author) or not isinstance(magazine, Magazine):
            raise TypeError("Author and Magazine must be of type Author and Magazine")
        
        # Set instance variables
        self._title = title
        self.content = content
        self.author_id = author.id
        self.magazine_id = magazine.id

        # Add the article to the database and get the article ID
        self.id = self.add_Article()

    @property
    def title(self):
        # Getter for title property
        return self._title

    @title.setter
    def title(self, title):
        # Ensure the title can only be set once
        if hasattr(self, '_title'):
            raise AttributeError("Article title cannot be changed")
        
        # Validate title type and length
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise AttributeError('title must be a string and between 5 and 50 characters')
        
        # Set the title
        self._title = title

    def __repr__(self):
        # Representation of the Article instance
        return f'<Article {self.title}>'

    def add_Article(self):
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL command to insert the article into the database
        sql = """
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
        """

        # Execute the command and commit the changes
        cursor.execute(sql, (self._title, self.content, self.author_id, self.magazine_id))
        conn.commit()

        # Get the ID of the newly created article
        article_id = cursor.lastrowid

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the article ID
        return article_id

    def get_Author(self):
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL command to get the author's name based on author_id
        sql = """
            SELECT name
            FROM authors
            WHERE id = ?
        """

        # Execute the command and fetch the result
        cursor.execute(sql, (self.author_id,))
        author_name = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the author's name
        return author_name

    def get_magazine(self):
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # SQL command to get the magazine's name based on magazine_id
        sql = """
            SELECT name
            FROM magazines
            WHERE id = ?
        """

        # Execute the command and fetch the result
        cursor.execute(sql, (self.magazine_id,))
        magazine_name = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the magazine's name
        return magazine_name

    @classmethod
    def create_article(cls, author, magazine, title, content):
        # Class method to create a new Article instance
        return cls(author, magazine, title, content)


