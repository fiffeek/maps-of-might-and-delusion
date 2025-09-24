# Maps of Might and Delusion

An AI-powered map generator for Heroes of Might and Magic III (VCMI) that uses Large Language Models to create unique, thematic template maps with intelligent object placement and terrain generation.

## Screenshots

There were taken in VCMI map generator, `./examples/configs/48L_brawl.yaml` (or static `./dist/momd/content/48L_brawl.JSON` with seed `42`):

<img width="1916" height="1912" alt="ss_2025-09-24_20:35:16" src="https://github.com/user-attachments/assets/4fac03dd-866b-4c60-b6c2-5968f173abf6" />

**Disclaimer**: These are assets from the original game, I nor VCMI owns them.

## Features

- AI-Driven Generation: Uses LLMs (OpenAI, Anthropic Claude) to generate creative and balanced VCMI maps
- Template System: Jinja2-based templates for flexible map generation logic
- Thematic Maps: Generate maps based on themes like Game of Thrones, mazes, or custom configurations
- Configurable: YAML-based configuration system for customizing generation parameters

## How It Works

The generator combines AI creativity with game mechanics knowledge:

1. **Template Processing**: Jinja2 templates define map structure and generation logic
2. **AI Planning**: LLMs analyze the template and plan object placement based on game balance and theme
3. **Map Creation**: The system generates VCMI-compatible `.json` map template files
4. **Validation**: Ensures generated maps meet VCMI requirements and are playable

## Usage

### Basic

Generate a map using a configuration file, in `./examples/configs/custom.yaml`
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


The map and the `VCMI` mod-info will be available there.
For one-off tests you can move it to `$HOME/.local/share/vcmi/Mods/` and enable the mod in `vcmilauncher`
prior to using the templates.

### Regular workflow
I link the mod directory to this repo, since in `dist` are the vetted templates that should play well:
```bash
REPO_LOCATION="~/personal/vcmi-llm-map-generator/dist/momd"
ln -s "$REPO_LOCATION" "$HOME/.local/share/vcmi/Mods/momd"
```

Then for generation, you can, in `./examples/configs/custom.yaml`
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

Maps are configured using YAML files that define:

- Map size and terrain preferences
- AI model settings and prompts
- Object placement rules and restrictions
- Thematic elements and constraints

See `examples/configs/` for sample configurations.

## Stats

For large map without an underground:
- 20k input tokens
- 8k output tokens


## Development Requirements

- asdf (for version management)
- `make`

```bash
# installs uv, pulls are dependencies and sets up git hooks
make dev
```
