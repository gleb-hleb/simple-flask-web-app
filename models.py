from sqlalchemy import Boolean, Column, Integer, String

from db import Base


# This class is used to create the users table in the database
# Of course it can be extended with more fields, but time for task was limited.
# It represents basic functionality for test task purposes.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_admin = Column(Boolean)

    def __repr__(self):
        """
        This function is called when you try to print an instance of the class
        :return: The id, username, and is_admin of the user.
        """
        return f"{self.id}: {self.username} {self.is_admin}"
