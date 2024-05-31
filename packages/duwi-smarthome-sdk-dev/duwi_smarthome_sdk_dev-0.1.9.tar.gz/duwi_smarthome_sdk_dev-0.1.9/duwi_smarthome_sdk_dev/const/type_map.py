# device_type
type_map = {
    "SWITCH": {
        "1-002": "On",
        "1-003": "On",
        "1-005": "On",
        "1-006": "On",
        "107-001": "On",
    },
    "LIGHT": {
        "1-001": "On",
        "1-004": "On",
        "3-001": "Dim",
        "3-002": "Temp",
        "3-003": "DimTemp",
        "3-004": "RGBW",
        "3-005": "RGB",
        "3-006": "RGBCW",
    },
    "COVER": {
        "4-001": "Roll",
        "4-002": "Roll",
        "4-003": "Shutter",
        "4-004": "Shutter",
    },
}

media_type_map = {
    "8-001-001": "HuaErSiMusic",
    "8-001-002": "XiangWangMusicS7Mini3S",
    "8-001-003": "XiangWangMusicS8",
    "8-001-004": "ShengBiKeMusic",
    "8-001-005": "BoShengMusic",
    "8-001-006": "SonosMusic",
}

sensor_type_map = {
    "7-001-001": ["temperature"],
    "7-002-001": ["humidity"],
    "7-003-001": ["light"],
    "7-004-001": ["formaldehyde"],
    "7-005-001": ["pm25"],
    "7-006-001": ["carbon_dioxide"],
    "7-007-001": ["air_quality"],
    "7-008-001": ["human"],
    "7-008-002": ["human"],
    "7-008-003": ["human", "light"],
    "7-009-001": ["trigger"],
    "7-009-002": ["human"],
    "7-009-003": ["human", "light"],
    "7-009-004": ["trigger"],
    "7-009-005": ["trigger"],
    "7-009-006": ["trigger"],
    "7-009-007": ["trigger"],
    "7-009-008": ["trigger"],
    "7-009-009": ["human"],
    "7-009-010": ["human"],
    "7-010-001": ["carbon_monoxide"],
    "7-011-001": ["tvoc"],
    "7-012-001": ["temperature", "humidity", "tvoc", "pm25", "formaldehyde", "carbon_dioxide", "pm10"],
    "7-012-002": ["carbon_monoxide"],
    "7-013-001": ["light", "human"],
}
group_type_map = {
    "SWITCH": {
        "Breaker": "On",
    },
    "LIGHT": {
        "Light": "Dim",
        "Color": "Temp",
        "LightColor": "DimTemp",
        "RGBW": "RGBW",
        "RGB": "RGB",
    },
    "COVER": {
        "Retractable": "Roll",
        "Roller": "Roll",
    },
}
