from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping

import yaml


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class KeywordWeights:
    positive: Dict[str, int]
    negative: Dict[str, int]


@dataclass(frozen=True)
class Filters:
    naics_include: List[str]
    preferred_notice_types: List[str]
    exclude_notice_types: List[str]
    posted_from_days: int


@dataclass(frozen=True)
class Scoring:
    include_in_digest_score: int
    naics_match_boost: int
    notice_type_boost: int
    set_aside_boost: int
    deadline_urgency_boost: int


@dataclass(frozen=True)
class Digest:
    max_items: int


@dataclass(frozen=True)
class Config:
    filters: Filters
    keywords: KeywordWeights
    scoring: Scoring
    digest: Digest


REQUIRED_TOP_LEVEL_KEYS = {"filters", "keywords", "scoring", "digest"}


def _require_keys(mapping: Mapping[str, Any], keys: set[str], context: str) -> None:
    missing = keys - set(mapping.keys())
    if missing:
        raise ConfigError(f"Missing required keys in {context}: {sorted(missing)}")


def _require_type(value: Any, expected_type: type, context: str) -> None:
    if not isinstance(value, expected_type):
        raise ConfigError(f"Expected {context} to be {expected_type.__name__}")


def _validate_keywords(keywords: Mapping[str, Any]) -> KeywordWeights:
    _require_keys(keywords, {"positive", "negative"}, "keywords")
    positive = keywords["positive"]
    negative = keywords["negative"]
    _require_type(positive, dict, "keywords.positive")
    _require_type(negative, dict, "keywords.negative")
    return KeywordWeights(
        positive={str(k).lower(): int(v) for k, v in positive.items()},
        negative={str(k).lower(): int(v) for k, v in negative.items()},
    )


def _validate_filters(filters: Mapping[str, Any]) -> Filters:
    _require_keys(
        filters,
        {"naics_include", "preferred_notice_types", "exclude_notice_types", "posted_from_days"},
        "filters",
    )
    naics = filters["naics_include"]
    preferred = filters["preferred_notice_types"]
    exclude = filters["exclude_notice_types"]
    posted_from_days = filters["posted_from_days"]
    _require_type(naics, list, "filters.naics_include")
    _require_type(preferred, list, "filters.preferred_notice_types")
    _require_type(exclude, list, "filters.exclude_notice_types")
    if not isinstance(posted_from_days, int) or posted_from_days < 0:
        raise ConfigError("filters.posted_from_days must be a non-negative integer")
    return Filters(
        naics_include=[str(code) for code in naics],
        preferred_notice_types=[str(item) for item in preferred],
        exclude_notice_types=[str(item) for item in exclude],
        posted_from_days=posted_from_days,
    )


def _validate_scoring(scoring: Mapping[str, Any]) -> Scoring:
    _require_keys(
        scoring,
        {
            "include_in_digest_score",
            "naics_match_boost",
            "notice_type_boost",
            "set_aside_boost",
            "deadline_urgency_boost",
        },
        "scoring",
    )
    return Scoring(
        include_in_digest_score=int(scoring["include_in_digest_score"]),
        naics_match_boost=int(scoring["naics_match_boost"]),
        notice_type_boost=int(scoring["notice_type_boost"]),
        set_aside_boost=int(scoring["set_aside_boost"]),
        deadline_urgency_boost=int(scoring["deadline_urgency_boost"]),
    )


def _validate_digest(digest: Mapping[str, Any]) -> Digest:
    _require_keys(digest, {"max_items"}, "digest")
    max_items = digest["max_items"]
    if not isinstance(max_items, int) or max_items <= 0:
        raise ConfigError("digest.max_items must be a positive integer")
    return Digest(max_items=max_items)


def load_config(path: str | Path) -> Config:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}
    _require_type(raw, dict, "config root")
    _require_keys(raw, REQUIRED_TOP_LEVEL_KEYS, "config root")
    filters = _validate_filters(raw["filters"])
    keywords = _validate_keywords(raw["keywords"])
    scoring = _validate_scoring(raw["scoring"])
    digest = _validate_digest(raw["digest"])
    return Config(filters=filters, keywords=keywords, scoring=scoring, digest=digest)


def config_to_dict(config: Config) -> Dict[str, Any]:
    return dataclasses.asdict(config)
