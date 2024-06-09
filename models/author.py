import sqlite3
class Author:
    def __init__(self, name):
        if not isinstance(name, str) or not name:
            raise ValueError(
                "Name must be a non-empty string"
            )
        self.id = None
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def name(self):
        return self._name
    @property
    def id(self):
        return self._id

    def save(self):
        """ Insert a new row with the name and location values of the current Department instance.
        Update object id attribute using the primary key value of new row.
        """
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self