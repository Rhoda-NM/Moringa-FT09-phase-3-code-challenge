from database.connection import get_db_connection
class Magazine:

    all={}
    def __init__(self, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")
        self.id = None
        self._name = name
        self._category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        if not isinstance(category, str) or not category:
            raise ValueError("Category must be a non empty string ")
        self._category = category

    def save(self):
        """ Insert a new row to the magazines table, and Update object id attribute using the primary key value of new row.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO magazines(name, category)
            VALUES (?, ?)
        """

        cursor.execute(sql, (self._name, self._category))
        conn.commit()

        self.id = cursor.lastrowid
        type(self).all[self.id] = self
        conn.commit()
        cursor.close()
        conn.close()

    def articles(self):
        """Return list of articles associated with current magazine instance"""
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            SELECT articles.*
            FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        """
        cursor.execute(sql, (self.id,))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [
            Article.instance_from_db(row) for row in rows
        ]

    def contributors(self):
        """Returns a list of Authors associated with a Magazine."""
        conn=get_db_connection()
        cursor= conn.cursor()
        sql="""
           SELECT name
           FROM authors
           WHERE id IN (SELECT author_id FROM articles WHERE magazine_id = ?)
           """
        cursor.execute(sql,(self.id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        authors = [row[0] for row in rows]
        return authors

    def article_titles(self):
        """Returns a list of article titles associated with a magazine """
        conn = get_db_connection()
        cursor=conn.cursor()
        sql="""
           SELECT title
           FROM articles
           WHERE magazine_id = ?
           """
        cursor.execute(sql,(self.id,))
        rows = cursor.fetchall()
        titles=[title[0] for title in rows]
        cursor.close()
        conn.close()
        if not titles:
            return None
        return titles

    def contributing_authors(self):
        from models.author import Author
        magazine_articles = self.articles()
        author_count = {}
        for article in magazine_articles:
            author_name = article.author.name
            author_count[author_name] = author_count.get(author_name, 0) + 1
        cont_authors = [author_name for author_name, article_count in author_count.items() if article_count > 2]
        if not cont_authors:
            return None
        return[author for author in Author.all if author.name in cont_authors]
