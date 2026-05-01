from __future__ import annotations

COMPANIES = {
    "AVNX": {
        "ticker": "AVNX",
        "name": "Avanex Therapeutics",
        "sector": "Biotech — oncology",
        "founded": 2014,
        "hq": "Cambridge MA",
    },
    "RPSE": {
        "ticker": "RPSE",
        "name": "Rapid Sense Robotics",
        "sector": "Industrial automation",
        "founded": 2009,
        "hq": "Pittsburgh PA",
    },
    "MCLD": {
        "ticker": "MCLD",
        "name": "Meridian Cloud Systems",
        "sector": "Enterprise SaaS — observability",
        "founded": 2016,
        "hq": "Austin TX",
    },
    "BRYL": {
        "ticker": "BRYL",
        "name": "Beryl Lithium",
        "sector": "Materials — battery-grade lithium",
        "founded": 2018,
        "hq": "Reno NV",
    },
    "PNVA": {
        "ticker": "PNVA",
        "name": "Penova Logistics",
        "sector": "Freight — last-mile",
        "founded": 2011,
        "hq": "Atlanta GA",
    },
    "QXLR": {
        "ticker": "QXLR",
        "name": "Quixar AI Compute",
        "sector": "Hardware — inference accelerators",
        "founded": 2020,
        "hq": "Santa Clara CA",
    },
}

MARKET_SNAPSHOTS = {
    "AVNX": {"price": 42.18, "market_cap_usd": 1_280_000_000, "pe_ratio": None, "ytd_change_pct": -8.4},
    "RPSE": {"price": 117.05, "market_cap_usd": 4_900_000_000, "pe_ratio": 28.6, "ytd_change_pct": 22.1},
    "MCLD": {"price": 89.72, "market_cap_usd": 7_400_000_000, "pe_ratio": 41.2, "ytd_change_pct": 14.7},
    "BRYL": {"price": 6.48, "market_cap_usd": 312_000_000, "pe_ratio": None, "ytd_change_pct": -38.2},
    "PNVA": {"price": 24.91, "market_cap_usd": 1_100_000_000, "pe_ratio": 16.4, "ytd_change_pct": 3.5},
    "QXLR": {"price": 308.44, "market_cap_usd": 22_600_000_000, "pe_ratio": 64.1, "ytd_change_pct": 71.8},
}

NEWS = {
    "AVNX": [
        {"date": "2026-04-22", "source": "FierceBiotech", "headline": "Avanex Phase II oncology readout misses primary endpoint"},
        {"date": "2026-04-10", "source": "Endpoints", "headline": "Avanex hires former Genentech CFO"},
    ],
    "RPSE": [
        {"date": "2026-04-29", "source": "Reuters", "headline": "Rapid Sense lands $180M auto-OEM contract"},
        {"date": "2026-04-12", "source": "WSJ", "headline": "Rapid Sense Q1 beats on margin expansion"},
    ],
    "MCLD": [
        {"date": "2026-04-18", "source": "TechCrunch", "headline": "Meridian Cloud acquires log-analytics vendor for $240M"},
    ],
    "BRYL": [
        {"date": "2026-04-25", "source": "Bloomberg", "headline": "Beryl Lithium delays Nevada plant by 8 months on permitting"},
        {"date": "2026-03-31", "source": "Reuters", "headline": "Lithium spot prices fall 14% QoQ"},
    ],
    "PNVA": [
        {"date": "2026-04-21", "source": "Logistics Weekly", "headline": "Penova trims 6% of workforce in route-density optimization"},
    ],
    "QXLR": [
        {"date": "2026-04-30", "source": "The Information", "headline": "Quixar's H4 chip ships in Q3, undercuts Nvidia on perf/$"},
        {"date": "2026-04-17", "source": "Reuters", "headline": "Quixar adds three hyperscaler customers"},
    ],
}
