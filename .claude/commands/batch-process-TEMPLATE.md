---
description: Run batch processing with preset configuration (TEMPLATE)
---

<!--
TEMPLATE: Customize this command for your project's batch processing needs.
Rename to match your use case (e.g., batch-build.md, batch-test.md, batch-convert.md)
-->

Execute batch processing using a preset configuration.

## Arguments

Parse the user's input for:
- `preset`: Name of preset from config (required)
- `--settings`: Named settings override (e.g., `fast`, `debug`, `production`)
- `--workers`: Override parallel worker count
- `--dry-run`: List items without processing

## Steps

1. **Load configuration**: Load project config files:
   ```python
   # Adapt to your project's config structure
   from utils.config_loader import load_config
   config = load_config('config/')
   ```

2. **Resolve preset**: Get the preset and resolve references:
   - Get preset definition from config
   - Resolve input sources/paths
   - Merge base settings with any overrides

3. **Collect input files**: For each source:
   - Build full path from config
   - Collect files using pattern matching
   - Report file count per source

4. **Display summary** before processing:
   ```
   Preset: [preset_name]
   Sources: [count] ([source_list])
   Files: [count] files
   Settings: [key settings]
   Output: [output_path]
   ```

5. **If dry-run**: Stop here and show what would be processed.

6. **Execute processing**:
   - Create output directory (timestamped if appropriate)
   - Configure processor with resolved settings
   - Run batch processor
   - Report results (success/failed/skipped counts)

7. **Report completion**:
   ```
   Completed: [X] success, [Y] failed, [Z] skipped
   Output: [output_path]
   ```

## Example Usage

```
/batch-process preset_name
/batch-process preset_name --settings debug
/batch-process preset_name --dry-run
/batch-process preset_name --workers 4
```

## Error Handling

- If preset not found: List available presets
- If source path not found: Report which source failed
- If no input files found: Warn and confirm before proceeding
