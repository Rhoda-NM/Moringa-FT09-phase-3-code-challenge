from __init__ import CURSOR, CONN
class Magazine:
    def __init__(self, id, name, category):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string")
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def id(self):
        return self._id
    
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

    def articles(self):
        """Return list of articles associated with current magazine instance"""
        from article import Article
        sql = """
            SELECT articles.*
            FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazine.id = ?
        """
        CURSOR.execute(sql, (self.id,),)

        rows = CURSOR.fetchall()
        return [
            Article.instance_from_db(row) for row in rows
        ]

    def contributors(self):
        pass

    def article_titles(self):
        pass

    def contributing_authors(self):
        pass
