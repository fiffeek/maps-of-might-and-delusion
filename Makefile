STAMP_DIR := stamp
PRECOMMIT_FILE := .pre-commit-config.yaml
PACKAGE_LOCK := package-lock.json
PYPROJECT := pyproject.toml
VENV := venv
UV_TOOL_DIR := $(abspath tools)
UV_TOOL_BIN_DIR := $(abspath bin)
UV_BIN := uv
UVX_BIN := uvx
NPM_BIN := npm
DOCKER_BIN := docker
VCMI_DIR := vcmi
HOMM_DATA_PATH ?=
XAUTH_PATH ?=

export UV_TOOL_DIR
export UV_TOOL_BIN_DIR
export PATH := $(UV_TOOL_BIN_DIR):$(PATH)

.PHONY: pre-commit pre-push

dev: \
	$(STAMP_DIR)/.dir.stamp \
	$(STAMP_DIR)/.asdf.stamp \
	$(STAMP_DIR)/.uv.stamp \
	$(STAMP_DIR)/.precommit.stamp \
	$(STAMP_DIR)/.formatters.stamp \
	$(STAMP_DIR)/.npm.stamp

$(STAMP_DIR)/.npm.stamp: $(PACKAGE_LOCK) $(STAMP_DIR)/.asdf.stamp
	@$(NPM_BIN) install
	@touch $@

$(STAMP_DIR)/.dir.stamp:
	@mkdir -p $(STAMP_DIR)
	@touch $@

$(STAMP_DIR)/.asdf.stamp:
	@asdf install
	@touch $@

$(STAMP_DIR)/.precommit.stamp: $(PRECOMMIT_FILE) $(STAMP_DIR)/.uv.stamp
	@$(UV_BIN) tool install pre-commit --with pre-commit-uv
	@$(UVX_BIN) pre-commit install && \
		$(UVX_BIN) pre-commit install --hook-type commit-msg
	@touch $@

$(STAMP_DIR)/.formatters.stamp: $(STAMP_DIR)/.uv.stamp
	@$(UV_BIN) tool install ruff
	@touch $@

$(STAMP_DIR)/.uv.stamp: $(STAMP_DIR)/.asdf.stamp $(PYPROJECT)
	@$(UV_BIN) sync
	@touch $@

pre-commit:
	@$(UVX_BIN) pre-commit

fmt:
	@$(UVX_BIN) ruff format

lint:
	@$(UVX_BIN) ruff check --fix

pre-push: pre-commit

build/container:
	@$(DOCKER_BIN) build -t momd:dev .
