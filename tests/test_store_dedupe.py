from pathlib import Path

from ceradon_sam_bot.store import init_db, upsert_opportunity


def test_store_dedupe(tmp_path: Path):
    db_path = tmp_path / "test.sqlite"
    init_db(db_path)
    normalized = {
        "notice_id": "ABC123",
        "solicitation_number": "SOL-1",
        "posted_date": "2024-01-01",
        "agency": "Test Agency",
        "title": "Test Title",
        "notice_type": "Sources Sought",
        "naics": "541715",
        "set_aside": "Small Business",
        "response_deadline": "2024-02-01",
        "link": "https://sam.gov/opp/ABC123/view",
    }
    raw = {"noticeId": "ABC123"}

    first = upsert_opportunity(db_path, normalized, raw, 10, ["reason"])
    second = upsert_opportunity(db_path, normalized, raw, 10, ["reason"])

    assert first is True
    assert second is False
