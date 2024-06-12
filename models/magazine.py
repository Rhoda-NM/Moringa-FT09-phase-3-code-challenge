from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category):
        self._name = name
        self._category = category
        self.id=self.add_magazine_to_db()
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if not isinstance(name,str) or not (2<=len(name)<=16):
            raise AttributeError('name must be a string and between 2 and 16 characters')
        self._name = name
    @property
    def category(self):
        return self._category
    @category.setter
    def category(self, category):
        if not isinstance(category,str) or not category :
            raise AttributeError('category must be a string and between 2 and 16 characters')
        self._category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    def add_magazine_to_db(self):
        conn=get_db_connection()
        cursor= conn.cursor()
        """create a new Magazine entry in the table"""
        sql="""
           INSERT INTO magazines (name, category)
           VALUES (?, ?)
           """
        cursor.execute(sql,(self._name, self._category))
        magazine_id = cursor.lastrowid 
        conn.commit()
        cursor.close()
        conn.close()
        return magazine_id
    @classmethod
    def create_magazine(cls,name,category):
        """Create a new Magazine instance"""
        return cls(name,category)
    def articles(self):
        """Return a list of articles"""
        conn=get_db_connection()
        cursor= conn.cursor()
        sql="""
           SELECT title
           FROM articles
           WHERE magazine_id = ?
           """
        cursor.execute(sql,(self.id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    def contributers(self):
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
        return rows
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
        return titles
    def contributing_authors(self):
        conn =get_db_connection()
        cursor = conn.cursor()
        sql = """
           SELECT name
           FROM authors
           WHERE id IN (SELECT author_id FROM articles WHERE magazine_id = ?)
           """
        cursor.execute(sql, (self.id,))
        rows = cursor.fetchall()
        authors = [row[0] for row in rows]
        cursor.close()
        return authors
