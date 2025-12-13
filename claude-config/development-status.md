# Development Status

**Last Updated**: 2025-12-12
**Development Notes**: `project-notes/development-notes-archive/development-notes_000.md` through `development-notes_020.md`

## Current State

**Project Phase**: Universal Skeleton Configuration System implemented

**Latest Session** (020 - 2025-12-12): Implemented data-driven skeleton profile system. Bone naming and coordinate transforms are now loaded from JSON profile files instead of hard-coded dictionaries. New skeleton formats can be added without code changes.

## Key Capabilities

- **Skeleton Profiles**: JSON-based configuration for bone mapping and coordinate transforms
- **Auto-Detection**: Automatic skeleton format detection from bone names
- **FBX Processing**: Batch export to .unsanim with multi-format skeleton support
- **Canonical Coordinates**: Maya-compatible output (right-handed, Y-up, Z-forward, cm units)
- **.unsanim Format**: Domain-agnostic animation storage with coordinate system metadata
- **Voxel+IDW Model**: Production model achieving 8.59deg angular error

## Canonical Coordinate System

```
Handedness: Right-handed
Up axis: +Y
Forward axis: +Z (character faces +Z)
Base unit: centimeters (cm)
```

## Supported Skeleton Formats

| Profile | Status | Axis Remap |
|---------|--------|------------|
| Mixamo | Tested | Reference (none) |
| HumanIK | Tested | Yes |
| Unreal | Tested | Yes |
| Rigify | Defined | TBD |

## Next Steps

1. Verify output consistency with previous exports (regression test)
2. Test Rigify axis remap when needed
3. Add leg bone support to export pipeline
4. Document coordinate system specification
5. Maya C++ plugin development (when ready)

## Key Files

| Purpose | Location |
|---------|----------|
| Skeleton profiles | `python/config/skeleton_profiles/*.json` |
| Profile loader | `python/src/skeleton_profile.py` |
| Arm data extraction | `python/src/arm_data_extractor.py` |
| Profile test script | `python/scripts/test_skeleton_profile.py` |
| .unsanim visualization | `python/scripts/visualization/visualize_unsanim.py` |
| Batch FBX export | `python/scripts/batch_export_fbx.py` |
| Production model | `python/data/models/idw_model_2025-10-26-17.06.json` |

## Implementation Plan

Full plan for the skeleton configuration system: `plans/2025-12-12_universal-skeleton-configuration.md`
