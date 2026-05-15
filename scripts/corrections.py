# Two-level countries that should display their higher-level regions (level 1) by
# default instead of the more detailed subdivisions. Use adm0_a3 country codes.
DEFAULT_LEVEL_1: set[str] = {
    "FRA",
    "ESP",
    "ITA",
}

# Manual region assignments for subdivisions missing a region in the Natural Earth
# source data. Keyed by adm1_code. Add entries here to fix additional orphans.
REGION_OVERRIDES: dict[str, str] = {
    "JPN-1827": "Kyushu",         # Saga Prefecture
    "JPN-3500": "Kyushu",         # Nagasaki Prefecture
    "CHN-1178": "East China",     # Fujian
    "IND-20012": "North",         # Ladakh
    "IND-2474": "South",          # Andaman and Nicobar Islands
}
