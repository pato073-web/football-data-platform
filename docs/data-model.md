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

## Team

Represents a football club or team.

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique identifier for the team |
| name | String | Official team name |
| country_id | Integer | Country associated with the team |

**Relationship:** `country_id` references `Country.id`.

## SeasonTeam

Represents the participation of a team in a specific competition season.

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique identifier for the participation record |
| season_id | Integer | Season in which the team participates |
| team_id | Integer | Team participating in the season |

**Relationships:**

- `season_id` references `Season.id`.
- `team_id` references `Team.id`.

## Player

Represents a football player.

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique identifier for the player |
| name | String | Full name of the player |
| country_id | Integer | Player nationality |
| birth_date | Date | Player date of birth |

**Relationship:** `country_id` references `Country.id`.

## PlayerSeasonTeam

Represents a player's membership in a team during a specific season.

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique identifier for the record |
| player_id | Integer | Player associated with the record |
| season_team_id | Integer | Team and season associated with the player |
| start_date | Date | Date the player joined the team |
| end_date | Date, Nullable | Date the player left the team |

**Relationships:**

- `player_id` references `Player.id`.
- `season_team_id` references `SeasonTeam.id`.

## Match

Represents a football match played within a specific season.

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique identifier for the match |
| season_id | Integer | Season associated with the match |
| home_team_id | Integer | Home team |
| away_team_id | Integer | Away team |
| match_date | Date | Date of the match |
| kickoff_time | Time, Nullable | Scheduled kickoff time |
| home_score | Integer, Nullable | Goals scored by the home team |
| away_score | Integer, Nullable | Goals scored by the away team |
| status | String | Current status of the match |
| round | String, Nullable | Matchday or competition round |

**Relationships:**

- `season_id` references `Season.id`.
- `home_team_id` references `Team.id`.
- `away_team_id` references `Team.id`.
