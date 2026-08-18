# Data Model

This document describes the initial entities and relationships used by the Football Data Platform.

## Competition

- id
- name
- country

## Team

- id
- name
- country
- competition_id

## Player

- id
- name
- nationality
- birth_date
- team_id

## Match

- id
- competition_id
- home_team_id
- away_team_id
- match_date
- home_score
- away_score
