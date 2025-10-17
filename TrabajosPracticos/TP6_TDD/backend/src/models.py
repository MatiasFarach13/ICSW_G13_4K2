from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, Float, create_engine
)
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

    # Relación 1:N con Compra
    compras = relationship('Compra', back_populates='user', cascade="all, delete-orphan")

    # -------------------
    # Métodos de seguridad
    # -------------------
    def set_password(self, raw_password: str):
        """Genera un hash seguro a partir de la contraseña en texto plano."""
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Verifica que la contraseña proporcionada coincida con el hash guardado."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, raw_password)

    # -------------------
    # Métodos auxiliares
    # -------------------
    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"


class Compra(Base):
    __tablename__ = 'compras'

    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    cantidad = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    forma_pago = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    user = relationship('User', back_populates='compras')

    def __repr__(self):
        return f"<Compra id={self.id} total={self.total} forma_pago={self.forma_pago}>"


# ------------------------------------
# Funciones auxiliares de base de datos
# ------------------------------------

def create_sqlite_db(path: str = 'sqlite:///data.db'):
    """Crea la base de datos SQLite y devuelve el engine y la Session."""
    engine = create_engine(path, echo=False, future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    # Semillas solo para entornos de desarrollo / pruebas
    try:
        if 'memory' not in path:
            session = Session()
            if session.query(User).count() == 0:
                u1 = User(email='juan@example.com', name='Juan')
                u1.set_password('juanpass')
                u2 = User(email='ana@example.com', name='Ana')
                u2.set_password('anapass')
                session.add_all([u1, u2])
                session.commit()

                c1 = Compra(
                    fecha=date.today(), cantidad=2, total=15000.0,
                    forma_pago='Efectivo', user_id=u1.id
                )
                c2 = Compra(
                    fecha=date.today(), cantidad=1, total=10000.0,
                    forma_pago='Tarjeta', user_id=u2.id
                )
                session.add_all([c1, c2])
                session.commit()
            session.close()
    except Exception as e:
        print("Error inicializando datos de prueba:", e)

    return engine, Session


def get_or_create_user_by_email(session, email, name=None):
    """
    Busca un usuario por email o lo crea si no existe.
    Retorna el objeto User (nunca None).
    """
    user = session.query(User).filter_by(email=email).first()
    if user:
        return user
    user = User(email=email, name=name)
    session.add(user)
    session.commit()
    return user
