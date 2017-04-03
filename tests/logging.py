from flask_stupe.logging import log


def test_log(caplog):
    log.info("test logging")
    for record in caplog.records:
        assert "test logging" in record.message
        assert "flask_stupe" == record.name
