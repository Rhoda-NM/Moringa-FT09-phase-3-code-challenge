from __init__ import CURSOR, CONN
from author import Author
from magazine import Magazine
class Article:

    all = {}
    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise ValueError("Author must be an instance of Author class")
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of Magazine class")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")
        self.author = author
        self.magazine = magazine
        self.title = title
        self._id = None
        self.save()

    def __repr__(self):
        return f'<Article {self.title}>'
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not 5 <= len(value) <= 50:
            raise ValueError("Title must be a string between 5 and 50 characters long")
        self._title = value
    
    def save(self):
        """ Insert a new row with the author_id, magazine_id and title values of the current article instance.
        Update object id attribute using the primary key value of new row.
        """
        sql = """
            INSERT INTO articles (author_id, magazine_id, title) VALUES (?, ?, ?)"
        """

        CURSOR.execute(sql, (self.author.id, self.magazine.id, self.title))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @property
    def author(self):
        query = """
            SELECT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.id = ?
        """
        CURSOR.execute(query, (self.id,))
        author_data = CURSOR.fetchone()
        if author_data:
            author_id, author_name = author_data
            author = Author(author_name, author_id)
            return author
        return None
        


    @property
    def magazine(self):
        sql = """
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.id = ?
        """
        CURSOR.execute(sql, (self.id,))
        magazine_data = CURSOR.fetchone()
        if magazine_data:
            magazine_id, magazine_name, magazine_category = magazine_data
            magazine = Magazine(magazine_name, magazine_category, magazine_id)
            return magazine
        return None
    
    @classmethod
    def instance_from_db(cls, row):
        """Return an article object having the attribute values from table row."""

        #check the dictionary for existing instance using the row's primary key
        article = cls.all.get(row[0])
        if article:
            #ensure attributes match row values in case local instance was modified
            article.author = row[1]
            article.magazine = row[2]
            article.title = row[3]
        else:
            # not in dictionary, create new instance and add to dictionary
            article = cls(row[1], row[2], row[3])
            article.id = row[0]
            cls.all[article.id] = article

        return article
    

