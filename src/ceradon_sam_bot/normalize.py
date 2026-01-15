from __future__ import annotations

from typing import Any, Dict


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_opportunity(raw: Dict[str, Any]) -> Dict[str, Any]:
    notice_id = _stringify(raw.get("noticeId"))
    solicitation_number = _stringify(raw.get("solicitationNumber"))
    title = _stringify(raw.get("title"))
    agency = _stringify(raw.get("agency")) or _stringify(raw.get("fullParentPathName"))
    notice_type = _stringify(raw.get("noticeType"))
    naics = _stringify(raw.get("naicsCode")) or _stringify(raw.get("naics"))
    set_aside = _stringify(raw.get("typeOfSetAside")) or _stringify(raw.get("setAside"))
    posted_date = _stringify(raw.get("postedDate"))
    response_deadline = _stringify(raw.get("responseDeadLine")) or _stringify(
        raw.get("responseDeadline")
    )
    description = _stringify(raw.get("description")) or _stringify(raw.get("summary"))
    if not description:
        description = _stringify(raw.get("fullDescription"))
    link = ""
    if notice_id:
        link = f"https://sam.gov/opp/{notice_id}/view"
    elif solicitation_number:
        link = f"https://sam.gov/opp/search?keywords={solicitation_number}"

    return {
        "notice_id": notice_id,
        "solicitation_number": solicitation_number,
        "title": title,
        "agency": agency,
        "notice_type": notice_type,
        "naics": naics,
        "set_aside": set_aside,
        "posted_date": posted_date,
        "response_deadline": response_deadline,
        "description": description,
        "link": link,
        "raw": raw,
    }
