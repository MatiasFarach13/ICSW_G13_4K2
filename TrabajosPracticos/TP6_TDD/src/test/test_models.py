from src.models import create_sqlite_db, User, Compra
from datetime import date


def test_create_user_and_compra():
    engine, Session = create_sqlite_db('sqlite:///:memory:')
    session = Session()

    # create user
    user = User(email='test@example.com', name='Test User')
    session.add(user)
    session.commit()

    # create compra
    compra = Compra(fecha=date.today(), cantidad=2, total=15000.0, forma_pago='Tarjeta', user_id=user.id)
    session.add(compra)
    session.commit()

    # fetch and assert
    u = session.query(User).filter_by(email='test@example.com').one()
    assert u.name == 'Test User'
    assert len(u.compras) == 1
    c = u.compras[0]
    assert c.cantidad == 2
    assert c.total == 15000.0
    assert c.forma_pago == 'Tarjeta'

    session.close()
