from ceradon_sam_bot.config import Config, Digest, Filters, KeywordWeights, Scoring
from ceradon_sam_bot.scoring import score_opportunity


def test_score_opportunity_keywords_and_boosts():
    config = Config(
        filters=Filters(
            naics_include=["541715"],
            preferred_notice_types=["Sources Sought"],
            exclude_notice_types=[],
            posted_from_days=14,
        ),
        keywords=KeywordWeights(
            positive={"prototype": 4, "sensor": 3},
            negative={"construction": 5},
        ),
        scoring=Scoring(
            include_in_digest_score=10,
            naics_match_boost=4,
            notice_type_boost=3,
            set_aside_boost=2,
            deadline_urgency_boost=2,
        ),
        digest=Digest(max_items=10),
    )
    opportunity = {
        "title": "Prototype sensor experiment",
        "description": "",
        "agency": "DARPA",
        "naics": "541715",
        "notice_type": "Sources Sought",
        "set_aside": "Small Business",
        "response_deadline": "2030-01-01",
    }
    score, reasons = score_opportunity(opportunity, config)
    assert score >= 4 + 3 + 4 + 3 + 2
    assert any("keyword:prototype" in reason for reason in reasons)
