# WarbandRTX Redux

RTX Remix configuration for Mount & Blade: Warband, with one `rtx.conf` per GPU tier.
Nexus Mods: https://www.nexusmods.com/mbwarband/mods/6722

## Contents

| Folder | Target GPUs | `rtx.graphicsPreset` |
|---|---|---|
| `RTX 4080,4090,5080,5090` | High-end RTX 40/50 | 1 (High) |
| `5000 series` | Other RTX 50 | 2 (Medium) |
| `4000 series` | Other RTX 40 | 2 (Medium) |
| `3000 series` | RTX 30 | 2 (Medium) |
| `2000 series` | RTX 20 | 2 (Medium) |
| `Intel-AMD` | Intel Arc / AMD RX | 3 (Low) |

`rgl_config.txt` switches Warband to the DirectX 7 renderer
(`use_pixel_shaders = 0`, `use_vertex_shaders = 0`), which RTX Remix needs.

The option names target RTX Remix 1.5.x. `rtx.rayreconstruction.model` was
removed in Remix 1.6, which ignores it.

## How RTX Remix presets interact with this file

`rtx.graphicsPreset` uses this numbering: **0 = Ultra, 1 = High, 2 = Medium, 3 = Low, 4 = Custom**.

When the preset is 0–3, Remix writes its own values for these options into a
layer that takes priority over `rtx.conf`, so values for them in `rtx.conf` are ignored:

- `rtx.pathMinBounces`, `rtx.pathMaxBounces`
- `rtx.russianRouletteMaxContinueProbability`, `rtx.russianRoulette1stBounceMinContinueProbability`
- `rtx.denoiseDirectAndIndirectLightingSeparately`, `rtx.enableUnorderedResolveInIndirectRays`,
  `rtx.enableTransmissionApproximationInIndirectRays`
- `rtx.di.enableRayTracedBiasCorrection`, `rtx.restirGI.biasCorrectionMode`,
  `rtx.restirGI.useReflectionReprojection`
- `rtx.enableStochasticAlphaBlend`, `rtx.postfx.enable`
- `rtx.rayreconstruction.model` (Ultra/High use Transformer; Medium/Low use CNN)
- volumetrics quality, NEE cache, and the NRC quality preset

To make your own values for these options take effect, set `rtx.graphicsPreset = 4` (Custom).

The presets above keep this mod's intended ray reconstruction model for each tier:
Transformer on the high-end tier and CNN everywhere else. RTX 4090 and 5090
owners can try `rtx.graphicsPreset = 0` (Ultra).

Settings that players change in the Remix menu (Alt+X) are saved to `user.conf`.
`user.conf` overrides both the preset and `rtx.conf`. If a player says an update
had no effect, have them delete `user.conf`.

## Checking the files

```
python3 tools/check_configs.py
```

The script checks that:

- every tier defines the same options;
- the presets are valid and go from strongest tier to weakest;
- frame generation is off for tiers that don't support it;
- `rgl_config.txt` has no duplicate keys, has cheat mode off, and uses DX7 mode.

## Changelog

### Unreleased
- Fixed reversed `rtx.graphicsPreset` values. In 0.1, the RTX 40/50 tiers loaded
  **Low** and Intel/AMD loaded **High**. New values: high-end tier = High,
  RTX 20/30/40/50 = Medium, Intel/AMD = Low.
- `rgl_config.txt`: set `cheat_mode` to 0 (0.1 turned cheats on for every player)
  and removed a duplicate `enable_blood` line.
- Added `tools/check_configs.py`.

### 0.1 Beta
- Initial release.
