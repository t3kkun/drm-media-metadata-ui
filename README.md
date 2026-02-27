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
```
---

## How to Use

1. Place your encrypted media files under the `contents/` directory.
2. Generate metadata:

```bash
uv run python generate_db.py
```
3. Lauch the UI
```bash
uv run ui.py
```
4. Click thumbnails to launch playback via the official player.

---


## Further Information

A detailed design explanation (in Japanese) is available here:
```
🔗 https://note.com/t3kkun/n/n486fc8022df2
```
---

## Disclaimer

This project is an independent, unofficial tool designed to improve metadata visibility for locally stored encrypted media files.

It does not decrypt, modify, or bypass DRM systems.
Playback is handled exclusively by the official media player.

The author is not affiliated with any media provider and assumes no responsibility for misuse.
Users are responsible for complying with the terms of their media service and applicable laws.
