#!/usr/bin/env python3
"""Sanity checks for the WarbandRTX Redux config files.

Run from the repository root:  python3 tools/check_configs.py
Exits with status 1 if any check fails.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "WarbandRTX Redux Beta"

# RTX Remix enum: Ultra=0, High=1, Medium=2, Low=3, Custom=4 (Auto=5).
PRESET_NAMES = {0: "Ultra", 1: "High", 2: "Medium", 3: "Low", 4: "Custom", 5: "Auto"}

# Tiers from strongest to weakest. A weaker tier must never get a
# higher-quality (numerically lower) preset than a stronger tier.
TIER_ORDER = [
    "RTX 4080,4090,5080,5090",
    "5000 series",
    "4000 series",
    "3000 series",
    "2000 series",
    "Intel-AMD",
]

# Features that only exist on NVIDIA RTX 40/50 hardware.
NO_FRAMEGEN_TIERS = {"3000 series", "2000 series", "Intel-AMD"}


def parse(path):
    """Return (dict, duplicate_keys) for a 'key = value' file."""
    values, dups = {}, []
    for raw in path.read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        if not sep:
            continue
        key, value = key.strip(), value.strip()
        if key in values:
            dups.append(key)
        values[key] = value
    return values, dups


def main():
    errors = []
    tiers = {}
    for tier in TIER_ORDER:
        conf = ROOT / tier / "rtx.conf"
        if not conf.is_file():
            errors.append(f"missing: {conf}")
            continue
        values, dups = parse(conf)
        if dups:
            errors.append(f"{tier}: duplicate keys {dups}")
        tiers[tier] = values

    # Every tier should define the same set of options.
    if tiers:
        all_keys = set().union(*(v.keys() for v in tiers.values()))
        for tier, values in tiers.items():
            missing = sorted(all_keys - values.keys())
            if missing:
                errors.append(f"{tier}: missing keys {missing}")

    # Graphics preset must be valid and ordered by tier strength.
    prev_tier, prev_preset = None, None
    for tier in TIER_ORDER:
        if tier not in tiers:
            continue
        raw = tiers[tier].get("rtx.graphicsPreset")
        try:
            preset = int(raw)
        except (TypeError, ValueError):
            errors.append(f"{tier}: invalid rtx.graphicsPreset {raw!r}")
            continue
        if preset not in PRESET_NAMES:
            errors.append(f"{tier}: unknown rtx.graphicsPreset {preset}")
            continue
        print(f"{tier:26s} graphicsPreset = {preset} ({PRESET_NAMES[preset]})")
        if preset != 4 and prev_preset is not None and prev_preset != 4 and preset < prev_preset:
            errors.append(
                f"{tier} uses {PRESET_NAMES[preset]} but stronger tier "
                f"{prev_tier} uses {PRESET_NAMES[prev_preset]}"
            )
        if preset != 4:
            prev_tier, prev_preset = tier, preset

    for tier in NO_FRAMEGEN_TIERS & tiers.keys():
        if tiers[tier].get("rtx.dlfg.enable", "False") == "True":
            errors.append(f"{tier}: DLSS frame generation needs an RTX 40/50 GPU")

    # rgl_config.txt checks.
    rgl, dups = parse(ROOT / "rgl_config.txt")
    if dups:
        errors.append(f"rgl_config.txt: duplicate keys {dups}")
    if rgl.get("cheat_mode") != "0":
        errors.append("rgl_config.txt: cheat_mode should be 0 in a public release")
    for key in ("use_pixel_shaders", "use_vertex_shaders"):
        if rgl.get(key) != "0":
            errors.append(f"rgl_config.txt: {key} must be 0 (DX7 renderer) for RTX Remix")

    if errors:
        print("\nFAILED:")
        for e in errors:
            print("  - " + e)
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
