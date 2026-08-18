# Data Model

This document describes the entities and relationships used by the Football Data Platform.

## Country

Represents a country.

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique identifier for the country |
| name | String | Country name |
| code | String | Unique country code |

## Competition

Represents a football competition.

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique identifier for the competition |
| name | String | Official competition name |
| country_id | Integer, Nullable | Country associated with the competition |

**Relationship:** `country_id` references `Country.id`.

## Season

Represents a specific edition or season of a competition.

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique identifier for the season |
| competition_id | Integer | Competition associated with the season |
| name | String | Season name, for example 2025-26 |
| start_date | Date | Start date of the season |
| end_date | Date | End date of the season |

**Relationship:** `competition_id` references `Competition.id`.
