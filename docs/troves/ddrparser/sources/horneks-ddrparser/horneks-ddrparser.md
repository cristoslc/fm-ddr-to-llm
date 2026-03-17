---
source-id: "horneks-ddrparser"
title: "DDRparser - FileMaker Solution Documentation"
type: web
url: "https://horneks.no/ddrparser"
fetched: 2026-03-17T00:00:00Z
hash: "54f1eca6e8019f2edd93677ca42c78663cdd08e3b91a3defbb51fbcaeb35d209"
---

# DDRparser - FileMaker Solution Documentation

## Overview

**DDRparser** is a command-line utility designed to transform FileMaker Pro solution exports into readable, searchable text files. It enables developers to understand complex FileMaker systems using standard development tools like text editors and version control systems.

## Core Functionality

### Input Sources

The tool processes two types of FileMaker exports:

**Database Design Report (DDR)**
- Accessed via Tools > Database Design Report
- Creates a folder containing Solution.xml and individual XML files per database
- Available in FileMaker Pro for many years

**Save as XML Export**
- Accessed via Tools > Save a Copy as XML
- Generates a single comprehensive XML file
- Available in FileMaker Pro 19 and newer versions

### Output Format

DDRparser converts XML into organized plain-text files, creating one document per object (scripts, tables, layouts, etc.) sorted into logical folders. This structure supports browsing, searching, and version control workflows.

## Key Benefits

- **Searchability**: Locate scripts, fields, relationships, and custom functions across entire solutions
- **Version Control**: Enable Git integration for tracking changes and maintaining audit trails
- **Readability**: Transform opaque XML into human-friendly documentation
- **Navigation**: Simplify exploration of large, complex FileMaker projects
- **Offline Access**: Works independently without additional licensing requirements

## Primary Use Cases

1. **Script Verification** - Search for all references to modified scripts across the system
2. **Relationship Exploration** - Navigate complex relationship structures via text search
3. **Solution Understanding** - Study new systems with expanded calculations visible in definitions
4. **Change Management** - Use Git to document modifications, identify authors, and review historical versions

## GUI Tool

A FileMaker application provides an interface for the command-line utility, requiring the ACF plugin version 1.7.5.6 or higher. The GUI tool handles file selection, folder navigation, and XML validation before generating terminal commands.

## Available Downloads

- **DDRparser 1.4.1 Mac** - Complete package including GUI tool
- **ACF Plugin Mac Universal 1.7.8.4** - Required for GUI functionality

## Technical Notes

Git functions as a read-only historical archive in this workflow. All modifications to FileMaker files must occur within FileMaker itself; Git cannot push changes back to the original solution.
