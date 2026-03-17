---
source-id: "horneks-git-source-control-ddrparser"
title: "GIT Source Control for FileMaker? Meet DDRparser"
type: web
url: "https://horneks.no/git-source-control-for-filemaker-meet-ddrparser"
fetched: 2026-03-17T00:00:00Z
hash: "7a9110519faad2f9a96001c6eb76959aa9d11add369a7102073061ca907d6a84"
---

# GIT Source Control for FileMaker? Meet DDRparser

## Introduction

FileMaker developers face a significant challenge: tracking changes across complex solutions lacks transparency. **DDRparser** is a free, command-line tool that transforms FileMaker's Database Design Report (DDR) into searchable, version-controlled text files compatible with Git workflows.

The tool addresses a critical pain point. When tested with a customer solution producing a 1GB DDR XML export across four files, no web browser could load the HTML version. DDRparser parsed the entire dataset in just 18 seconds, making searching and diffing practical.

## Core Functionality

DDRparser performs these essential tasks:

- **Parses FileMaker DDR XML exports** into organized folder structures
- **Splits content by object type**: Scripts, Layouts, ValueLists, MenuSets, CustomFunctions, BaseTables, Relationships
- **Creates readable .txt files** suitable for text editors and search tools
- **Enables Git integration** with optional auto-commit capabilities
- **Integrates with development workflows** using BBEdit, VS Code, and Kaleidoscope for multi-file searches and diff operations

## Key Features

The tool offers impressive performance and flexibility:

- Handles multi-gigabyte DDR files in seconds
- Includes translation workflow tools for multilingual solutions
- Provides optional cleanup to remove outdated files
- Requires no plugins or licensing for core functionality
- Available for macOS (Intel + Apple Silicon) and Windows
- Includes optional FileMaker GUI tool powered by ACF plugin

## Output Structure

DDRparser organizes parsed content into logical folders:

**CustomMenus & MenuSets**: Menu definitions and associated layouts
**CustomFunctions**: Individual files per function with parameters and source code
**Scripts**: Complete scripts with step details and indentation
**ValueLists**: Centralized file listing all value lists and contents
**Layouts**: Object inventories useful for searching field references
**Relationships**: Comprehensive graph documentation with join predicates
**BaseTables**: Field listings including calculated formulas

## Practical Applications

The parsed output integrates seamlessly with professional development tools:

- **Multi-file searching** across entire solutions
- **Difference comparison** between development snapshots
- **Git version control** with automatic commit support
- **Change tracking** through repository history

## Licensing and Distribution

The tool is completely free with no licensing requirements for the core command-line application. An optional FileMaker GUI tool uses the ACF plugin, which includes a free license valid until September 1, 2025. After expiration, the plugin functions for 30 minutes per session -- sufficient for this utility.

Downloads are available on the HORNEKS ANS website for both macOS and Windows platforms, with SHA-256 checksums for integrity verification.
