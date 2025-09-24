# Maps of Might and Delusion III

An AI-powered map generator for Heroes of Might and Magic III (VCMI) that uses Large Language Models to create unique, thematic template maps with intelligent object placement and terrain generation.

## Screenshots

These were taken in VCMI map generator, using `./examples/configs/48L_brawl.yaml` (or static `./dist/momd/content/48L_brawl.JSON` with seed `42`):

<img width="500" height="499" alt="ss_2025-09-24_20-35-16" src="https://github.com/user-attachments/assets/804a9bd0-a4ad-4daf-bcae-029716d56582" />



**Disclaimer**: These are assets from the original game, neither I nor VCMI own them.

## Features

- **AI-Driven Generation**: Uses LLMs (OpenAI, Anthropic Claude) to generate creative and balanced VCMI maps
- **Template System**: Jinja2-based templates for flexible map generation logic
- **Thematic Maps**: Generate maps based on themes like Game of Thrones, mazes, or custom configurations
- **Configurable**: YAML-based configuration system for customizing generation parameters

## How It Works

The generator combines AI creativity with game mechanics knowledge:

1. **Template Processing**: Jinja2 templates define map structure and generation logic
2. **AI Planning**: LLMs analyze the template and plan object placement based on game balance and theme
3. **Map Creation**: The system generates VCMI-compatible `.json` map template files
4. **Validation**: Ensures generated maps meet VCMI requirements and are playable

## Usage

### Quick Start

Generate a map using a configuration file. Create `./examples/configs/custom.yaml`:
```yaml
llm_seed: 42
players: 8
humans: 8
map_size: m
freeform: |
  - add underground
save_path: /app/output
```

Then in command line:
```bash
docker pull ghcr.io/fiffeek/maps-of-might-and-delusion:latest
docker run \
  -v ./examples:/app/custom_examples \
  -v ./output:/app/output \
  -e ANTHROPIC_API_KEY='sk-...' \
  ghcr.io/fiffeek/maps-of-might-and-delusion:latest --debug generate --config-path /app/custom_examples/configs/custom.yaml
```


The map and the VCMI mod-info will be available in the output directory.
For one-off tests, move it to `$HOME/.local/share/vcmi/Mods/` and enable the mod in `vcmilauncher` before using the templates.

### Regular Workflow
Link the mod directory to this repo, since `dist` contains vetted templates that should play well:
```bash
REPO_LOCATION="~/personal/vcmi-llm-map-generator/dist/momd"
ln -s "$REPO_LOCATION" "$HOME/.local/share/vcmi/Mods/momd"
```

Then for generation, create `./examples/configs/custom.yaml`:
```yaml
llm_seed: 42
players: 8
humans: 8
map_size: l
template_name_override: "L88_Desert"
freeform: |
  - no underground
  - spawn a treasure zone next to each player starting zone with 1 town, they cant be desert nor snow
  - 3 other treasure zones with 1 town each, all desert, spawn more treasure here
  - 1 bigger treasure zone with 3 towns, snow, big time treasure here
  - give players more treasure in the starting area for faster gameplay
  - connections should be guarded
  - players 1-4 have zones close to one another (1 to 2, 2 to 3, 3 to 4), use fictive
  - players 5-8 have zones close to one another (5 to 6, 6 to 7, 7 to 8), use fictive
  - zones in (1-4) and (5-8) repel each other, put all 16 combinations
save_path: /app/dist/momd
```

And run with:
```bash
docker run \
  -v ./examples:/app/custom_examples \
  -v ./dist:/app/dist \
  -e ANTHROPIC_API_KEY='sk-...' \
  ghcr.io/fiffeek/maps-of-might-and-delusion:latest --debug generate --config-path /app/custom_examples/configs/custom.yaml
```

### Example Configurations

- `game_of_thrones.yaml` - Creates GoT-themed maps with houses and regions
- `maze.yaml` - Generates maze-like maps with strategic chokepoints
- `go_nuts.yaml` - Creates chaotic, resource-rich maps

## Configuration

Maps are configured using YAML files with the following options:

### Basic Configuration Options

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `llm_seed` | number | Random seed for consistent map generation (using disk cache) | `42` |
| `players` | number | Total number of player slots (1-8) | `8` |
| `humans` | number | Number of human players | `4` |
| `map_size` | string | Map size: `s` (small), `m` (medium), `l` (large), `xl` (extra large), ... | `l` |
| `save_path` | string | Directory to save generated maps | `/app/output` |
| `template_name_override` | string | Override the generated template name | `L84S` |
| `freeform` | string | Custom instructions for map generation (see below) | See examples |
| `prompt_template_overwrite` | string | Custom prompt template for the AI | Custom Jinja2 template |

### Freeform Instructions

The `freeform` field allows you to provide custom instructions to the AI for map generation. Common options include:

**Underground Control:**
- `no underground` - Disable underground level
- `add underground` - Enable underground level
- `underground serves as shortcuts` - Underground connects distant areas

**Zone Configuration:**
- `add N zones` - Create additional zones (e.g., `add 20 zones`)
- `place a choke point in the middle` - Create central contested area
- `treasure zone next to each player` - Personal expansion zones
- `N main treasure zone hubs with 1 town each` - Major contested areas

**Player Layout:**
- `place players in maximum distance between one another` - Spread players apart
- `players 1-4 have zones close to one another` - Create team clusters
- Use `fictive` connections for close player positioning
- Use `repel` for distant positioning (e.g., `put all 16 combinations`)

**Resource and Object Control:**
- `give players more treasure in starting zones` - Boost early game
- `give players more mines in starting zones` - Resource advantage
- `ban creature banks in starting zones` - Prevent early power spikes
- `ban pandora box` - Remove random artifacts
- `no teleporters on surface` - Limit mobility options
- `use as many custom objects as viable` - Enable mod objects

**Connection Types:**
- `do not use junction connections, prefer treasure or wide` - Control zone connections
- `the ONLY allowed connection type is forcePortal` - Portal-only connections
- `connections should be guarded` - Add guardians to passages

See `examples/configs/` for complete configuration examples.

## Stats

For large map without an underground:
- 20k input tokens
- 8k output tokens


## Development

### Requirements

- asdf (for version management)
- make

### Setup

```bash
# Install uv, pull dependencies, and set up git hooks
make dev
```
