import sqlite3


# Utlized https://stackoverflow.com/questions/67735813/format-kwargs-to-f-string
# for formatting kwargs to string ``" AND ".join([f"{k} = ?" for k in kwargs])``
# inspired by sqlalchemy orm

class Model:
    """Base class for all models, acts as an interface for all models
    """

    db_name = "db.sql"
    table_name = None
    
    @classmethod
    def _execute_query(cls, query, parameters=None):
        with cls.get_connection() as connection:
            cursor = connection.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            connection.commit()
            return cursor

    @classmethod
    def get_connection(cls):
        return sqlite3.connect(cls.db_name)
    
    @classmethod
    def create_table(cls):
        raise NotImplementedError
    
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.save()
        return instance
    
    @classmethod
    def get(cls, **kwargs):
        if not kwargs:
            raise ValueError("No filtering criteria provided")

        conditions = " AND ".join([f"{k} = ?" for k in kwargs])
        query = f"SELECT * FROM {cls.table_name} WHERE {conditions}"
        cursor = cls._execute_query(query, tuple(kwargs.values()))

        row = cursor.fetchone()
        if row:
            return cls(*row)
        return None

    @classmethod
    def get_all(cls):
        query = f"SELECT * FROM {cls.table_name}"
        cursor = cls._execute_query(query)
        return [cls(*row) for row in cursor.fetchall()]
    
    @classmethod
    def update(cls, **kwargs):
        instance = cls.get(**kwargs)
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    @classmethod
    def delete(cls, **kwargs):
        if not kwargs:
            raise ValueError("No filtering criteria provided")

        conditions = " AND ".join([f"{k} = ?" for k in kwargs])
        query = f"DELETE FROM {cls.table_name} WHERE {conditions}"
        cls._execute_query(query, tuple(kwargs.values()))
    
    def _insert(self, *args, **kwargs):
        columns = ", ".join(self.__dict__.keys())
        values = ", ".join(["?"] * len(self.__dict__))
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
        cursor = self._execute_query(query, tuple(self.__dict__.values()))
        self.id = cursor.lastrowid

    def _update(self):
        columns = ", ".join([f"{k} = ?" for k in self.__dict__.keys()])
        query = f"UPDATE {self.table_name} SET {columns} WHERE id = ?"
        parameters = tuple(self.__dict__.values()) + (self.id,)
        self._execute_query(query, parameters)
  
    def save(self, *args, **kwargs):
        if not self.id:
            self._insert()
        else:
            self._update()

