from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime
from passlib.hash import pbkdf2_sha256  # hashing password

# base setting database
Base = declarative_base()
DATABASE_URL = "sqlite:///poly_messenger.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Database Models
class User(Base):
    """user model"""
    tablename = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)  # hash password
    phone_number = Column(String(15), unique=True, nullable=False)
    profile_picture = Column(String(200), default="default_profile.jpg")
    bio = Column(String(200), default="")

    # relationship
    contacts = relationship("Contact", foreign_keys="[Contact.user_id]", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="[Message.receiver_id]", back_populates="receiver")


class Contact(Base):
    """user contact Model"""
    tablename = 'contacts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # relationship
    user = relationship("User", foreign_keys=[user_id], back_populates="contacts")
    contact = relationship("User", foreign_keys=[contact_id])


class Message(Base):
    """message Model"""
    tablename = 'messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String(1000), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    is_file = Column(Boolean, default=False)
    file_path = Column(String(200), nullable=True)
    is_read = Column(Boolean, default=False)

    # relationship
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")

