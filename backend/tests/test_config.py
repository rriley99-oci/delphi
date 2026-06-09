from app.core.config import Settings


def test_settings_read_database_url_from_delphi_env(monkeypatch):
    monkeypatch.setenv(
        "DELPHI_DATABASE_URL",
        "postgresql+psycopg://user:password@db.example.test:5432/delphi_test",
    )

    settings = Settings()

    assert (
        settings.database_url
        == "postgresql+psycopg://user:password@db.example.test:5432/delphi_test"
    )


def test_settings_keep_local_postgres_default():
    settings = Settings()

    assert settings.database_url.startswith("postgresql+psycopg://")
