from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=True)

    password_hash = Column(String(255), nullable=True)
    compras = relationship('Compra', back_populates='user')

    def set_password(self, raw_password: str):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, raw_password)

class Compra(Base):
    __tablename__ = 'compras'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    cantidad = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    forma_pago = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    user = relationship('User', back_populates='compras')

# helper to create an in-memory sqlite DB for tests / quick usage
def create_sqlite_db(path: str = 'sqlite:///:memory:'):
    engine = create_engine(path, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    # If this is a file-based sqlite DB (not in-memory), seed with mock users
    try:
        if 'memory' not in path:
            session = Session()
            # only seed when empty
            if session.query(User).count() == 0:
                # create two mock users
                u1 = User(email='juan@example.com', name='Juan')
                u1.set_password('juanpass')
                u2 = User(email='ana@example.com', name='Ana')
                u2.set_password('anapass')
                session.add_all([u1, u2])
                session.commit()
                # create some compras for them
                c1 = Compra(fecha=date.today(), cantidad=2, total=15000.0, forma_pago='Efectivo', user_id=u1.id)
                c2 = Compra(fecha=date.today(), cantidad=1, total=10000.0, forma_pago='Tarjeta', user_id=u2.id)
                session.add_all([c1, c2])
                session.commit()
            session.close()
    except Exception:
        # keep helper robust in environments without SQLAlchemy extras
        pass

    return engine, Session


def get_or_create_user_by_email(session, email, name=None):
    user = session.query(User).filter_by(email=email).first()
    if user:
        return user
    user = User(email=email, name=name)
    session.add(user)
    session.commit()
    return user
