import pytest
from fastapi.testclient import TestClient
from inventory.models import Location, Unit
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


from main import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_location(client: TestClient):
    response = client.post(
        "/location/", json={"name": "Källare"}
    )
    app.dependency_overrides.clear()
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Källare"


def test_read_locations(session: Session, client: TestClient):
    loc_1 = Location(name="Källare")
    loc_2 = Location(name="Stugan")
    session.add(loc_1)
    session.add(loc_2)
    session.commit()

    response = client.get("/location/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == loc_1.name
    assert data[0]["id"] == loc_1.id
    assert data[1]["name"] == loc_2.name
    assert data[1]["id"] == loc_2.id


def test_read_unit(session: Session, client: TestClient):
    unit_1 = Unit(name="Äppelkompot")
    session.add(unit_1)
    session.commit()

    response = client.get(f"/unit/{unit_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == unit_1.name
    assert data["id"] == unit_1.id


def test_update_unit(session: Session, client: TestClient):
    unit_1 = Unit(name="Äppelkompot")
    session.add(unit_1)
    session.commit()

    response = client.patch(f"/unit/{unit_1.id}", json={"name": "Äppelkompot söt"})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Äppelkompot söt"
    assert data["id"] == unit_1.id


def test_delete_unit(session: Session, client: TestClient):
    unit_1 = Unit(name="Äppelkompot")
    session.add(unit_1)
    session.commit()

    response = client.delete(f"/unit/{unit_1.id}")

    unit_in_db = session.get(Unit, unit_1.id)

    assert response.status_code == 200

    assert unit_in_db is None
