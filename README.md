# Maps of Might and Delusion

An AI-powered map generator for Heroes of Might and Magic III (VCMI) that uses Large Language Models to create unique, thematic template maps with intelligent object placement and terrain generation.

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

Generate a map using a configuration file:

TODO add docker container and run

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


## Development Requirements

- asdf (for version management)
- `make`

```bash
# installs uv, pulls are dependencies and sets up git hooks
make dev
```
