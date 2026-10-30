#!/usr/bin/env python3
"""Hungarian public holidays, Chinese-language iCalendar feed.

NOTE: 2026 workday swaps are manually curated from 10/2025 (IV.30.) NGM.
Future swaps must be added when officially announced; this is not a live
translation of Apple's source.
"""
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import argparse

NAMES = [
    ("0101", "元旦"),
    ("0315", "1848年革命纪念日"),
    ("0501", "劳动节"),
    ("0820", "圣伊什特万国王节（建国纪念日）"),
    ("1023", "1956年革命纪念日"),
    ("1101", "诸圣节"),
    ("1225", "圣诞节"),
    ("1226", "圣诞节第二天"),
]
SWAPS_2026 = [
    (date(2026, 1, 2), "调休休息日（补1月10日）"),
    (date(2026, 1, 10), "调休工作日（补1月2日）"),
    (date(2026, 8, 8), "调休工作日（补8月21日）"),
    (date(2026, 8, 21), "调休休息日（补8月8日）"),
    (date(2026, 12, 12), "调休工作日（补12月24日）"),
    (date(2026, 12, 24), "调休休息日（补12月12日）"),
]

def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f, g = (b + 8) // 25, (b - (b + 8) // 25 + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    p = h + l - 7 * m + 114
    return date(y, p // 31, p % 31 + 1)

def escape(s):
    return s.replace("\\", "\\\\").replace("\n", "\\n").replace(",", "\\,").replace(";", "\\;")

def fold(line):
    lines, part, size = [], "", 0
    for ch in line:
        n = len(ch.encode("utf-8"))
        if size + n > 75:
            lines.append(part)
            part, size = " ", 1
        part += ch
        size += n
    lines.append(part)
    return "\r\n".join(lines)

def generate(start=2026, end=2035):
    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0",
        "PRODID:-//Hungary Holidays Chinese//Calendar//ZH-CN",
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
        "X-WR-CALNAME:匈牙利节假日（中文）",
        "X-WR-CALDESC:匈牙利法定节假日及已公布调休",
        "X-WR-TIMEZONE:Europe/Budapest",
        "REFRESH-INTERVAL;VALUE=DURATION:P1D",
        "X-PUBLISHED-TTL:PT24H",
    ]
    events = []
    for y in range(start, end + 1):
        events.extend((date(y, int(mmdd[:2]), int(mmdd[2:])), name) for mmdd, name in NAMES)
        e = easter(y)
        events.extend([
            (e - timedelta(days=2), "耶稣受难日"),
            (e + timedelta(days=1), "复活节星期一"),
            (e + timedelta(days=50), "圣灵降临节星期一"),
        ])
    if start <= 2026 <= end:
        events.extend(SWAPS_2026)
    for d, name in sorted(events):
        typ = "workday" if "工作日" in name else ("rest" if "休息日" in name else "holiday")
        lines.extend([
            "BEGIN:VEVENT", f"UID:hu-zh-{d:%Y%m%d}-{typ}@hungary-holidays-zh",
            f"DTSTAMP:{now}",
            f"DTSTART;VALUE=DATE:{d:%Y%m%d}",
            f"DTEND;VALUE=DATE:{d + timedelta(days=1):%Y%m%d}",
            f"SUMMARY:{escape(name)}",
            "TRANSP:TRANSPARENT", "STATUS:CONFIRMED", "END:VEVENT",
        ])
    lines.append("END:VCALENDAR")
    return "\r\n".join(fold(s) for s in lines) + "\r\n", len(events)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=2026)
    parser.add_argument("--end", type=int, default=2035)
    parser.add_argument("--output", default="hungary-holidays-zh.ics")
    a = parser.parse_args()
    ics, count = generate(a.start, a.end)
    Path(a.output).write_bytes(ics.encode("utf-8"))
    print(f"Generated {count} events.")
