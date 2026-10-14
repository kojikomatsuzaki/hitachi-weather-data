"""チェックサム照合済みZIPの診断で確認した、年別原ファイルの不在だけを許可する。"""

# A missing member outside this explicit inventory remains an import error.
KNOWN_ABSENT_SOURCE_YEARS = {
    "dew_point_temperature": frozenset(range(1971, 1983)),
    "solar_radiation": frozenset(range(1971, 1981)),
    "sunshine_duration": frozenset({1977}),
}

ELEMENT_IDS = {
    "dew_point_temperature": "dew_point_temperature_c",
    "solar_radiation": "global_solar_radiation_mj_m2",
    "sunshine_duration": "sunshine_duration_h",
}

def absent_source_elements(year):
    return {key for key, years in KNOWN_ABSENT_SOURCE_YEARS.items() if year in years}
