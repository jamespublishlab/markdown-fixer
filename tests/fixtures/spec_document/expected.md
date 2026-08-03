# Widget Export Spec

## Overview

This document describes the widget export pipeline.

### Goals

- Export widgets to JSON
- Preserve ordering
- Support incremental export

### Non-Goals

1. Real-time sync
2. Cross-tenant export

- **Status:** Draft
- **Owner:** Platform Team

**Required fix.** Rebase this branch on main before merging: the export queue moved.

| Field   | Type    | Notes                  |
|:--------|:--------|:-----------------------|
| id      | string  | Primary key            |
| name    | string  | Display name           |
| version | integer | Bumped on every export |

The table above lists the export record shape.
