from app.core.config import Settings
from app.db.session import create_db_engine


def test_create_db_engine_uses_configured_database_url():
    settings = Settings(
        database_url="postgresql+psycopg://delphi:secret@localhost/delphi"
    )

    engine = create_db_engine(settings)

    assert engine.url.drivername == "postgresql+psycopg"
    assert engine.url.username == "delphi"
    assert engine.url.database == "delphi"
