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

Targets RTX Remix 1.6.1. Also works with 1.5.x.

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
- volumetrics quality, NEE cache, and the radiance cache (SHaRC/NRC) quality preset
- sparse rendering settings and, on Medium/Low, `rtx.dlfg.litePreset`

To make your own values for these options take effect, set `rtx.graphicsPreset = 4` (Custom).

RTX 4090 and 5090 owners can try `rtx.graphicsPreset = 0` (Ultra).

Remix 1.6 notes:
- Ray reconstruction always uses the Transformer model. The CNN option is gone.
- The default indirect lighting cache is SHaRC (`rtx.integrateIndirectMode = 3`).
  The `rtx.neuralRadianceCache.*` options only apply if NRC is selected.

Settings that players change in the Remix menu (Alt+X) are saved to `user.conf`.
`user.conf` overrides both the preset and `rtx.conf`. If a player says an update
had no effect, have them delete `user.conf`.

## Changelog

### 0.1.2 Beta
- Updated for RTX Remix 1.6.1: removed `rtx.rayreconstruction.model`, which
  Remix 1.6 no longer has. Remix 1.5.x users see no change, because there the
  graphics preset already chose the model.

### 0.1.1 Beta
- Fixed reversed `rtx.graphicsPreset` values. In 0.1, the RTX 40/50 tiers loaded
  **Low** and Intel/AMD loaded **High**. New values: high-end tier = High,
  RTX 20/30/40/50 = Medium, Intel/AMD = Low.
- `rgl_config.txt`: set `cheat_mode` to 0 (0.1 turned cheats on for every player)
  and removed a duplicate `enable_blood` line.

### 0.1 Beta
- Initial release.
