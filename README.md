# drm-media-metadata-ui

A DRM-respecting metadata viewer for locally stored encrypted media files.

This project improves the browsing experience of offline DRM-protected media
without modifying, decrypting, or bypassing any protection mechanisms.

---

## Overview

Some official offline media players require encrypted formats and provide
limited file-system visibility (no thumbnails, no metadata until playback).

This tool extracts metadata from local encrypted filenames,
generates thumbnail URLs based on public static patterns,
and provides a lightweight UI built with Flet to improve usability.

Playback is always handled by the official player via file association.

---

## What This Project Does

- Extracts content IDs from encrypted filenames
- Generates thumbnail URLs using known public patterns
- Optionally retrieves public metadata via search engines
- Builds a CSV metadata database
- Provides a local browsing UI (Flet-based)
- Launches the official media player for playback

---

## What This Project Does NOT Do

- ❌ Decrypt any content
- ❌ Bypass DRM
- ❌ Interact with private APIs
- ❌ Use authentication cookies
- ❌ Download media from any service

This project operates entirely on locally stored encrypted files.

---

## Architecture

Encrypted Files  
→ ID Extraction  
→ Thumbnail URL Generation  
→ Metadata CSV  
→ Flet UI  
→ Official Player

---

## Installation

```bash
uv sync
