from database.connection import get_db_connection
class Author:
    all = {}

    def __init__(self, name):
        self.id = None
        self._name = name
        self.save()

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if hasattr(self, '_name'):
            raise AttributeError("Name cannot be changed")
        if not isinstance(name, str) or not name:
            raise ValueError(
                "Name must be a non-empty string"
            )

    def save(self):
        """ Insert a new row with the name attribute, and Update object id attribute using the primary key value of new row.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO authors (name)
            VALUES (?)
        """

        cursor.execute(sql, (self.name,))
        conn.commit()

        self.id = cursor.lastrowid
        type(self).all[self.id] = self

    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
           SELECT title
           FROM articles
           WHERE author_id = ?
           """
        cursor.execute(sql, (self.id,))
        rows = cursor.fetchall()
        article_titles = [row[0] for row in rows]
        cursor.close()
        return article_titles

    def magazines(self):
        conn =get_db_connection()
        cursor = conn.cursor()
        sql = """
           SELECT name
           FROM magazines
           WHERE id IN (SELECT magazine_id FROM articles WHERE author_id = ?)
           """
        cursor.execute(sql, (self.id,))
        rows = cursor.fetchall()
        magazines = [row[0] for row in rows]
        cursor.close()
        return magazines