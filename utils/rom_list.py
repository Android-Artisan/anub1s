def get_official_roms_for_device(device_model):
    model = device_model.upper().replace(" ", "")

    rom_database = {
        "SM-G980F": [
            {
                "name": "ExtremeROM OneUI 7 Port",
                "url": "tbd"
            },
            {
                "name": "[EOL] ExtremeROM OneUI 6.1 Port",
                "url": "tbd"
            }
        ],
        "SM-G981B": [
            {
                "name": "ExtremeROM OneUI 7 Port",
                "url": "tbd"
            },
            {
                "name": "[EOL] ExtremeROM OneUI 6.1 Port",
                "url": "tbd"
            }
        ],
        "SM-G985F": [
            {
                "name": "ExtremeROM OneUI 7 Port",
                "url": "tbd"
            },
            {
                "name": "[EOL] ExtremeROM OneUI 6.1 Port",
                "url": "tbd"
            }
        ],
        "SM-G986B": [
            {
                "name": "ExtremeROM OneUI 7 Port",
                "url": "tbd"
            },
            {
                "name": "[EOL] ExtremeROM OneUI 6.1 Port",
                "url": "tbd"
            }
        ],
        "SM-G988B": [
            {
                "name": "ExtremeROM OneUI 7 Port",
                "url": "tbd"
            },
            {
                "name": "[EOL] ExtremeROM OneUI 6.1 Port",
                "url": "tbd"
            }
        ],
    }

    return rom_database.get(model, [])
