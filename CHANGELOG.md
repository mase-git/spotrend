# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2023-01-23

### Added
- Added basic function to retrieves formatted dictionary for tracks, artists and album information
- Defined function to setup the authentication and oauth2 credentials according to the Spotify API usage.
- Defined function to retrieves audio features in a well formatted form
- Implemented basic unit test

### Unrelease
This is a baseline using existing Spotipy. Next version will use standalone function for a direct Spotify API integration.
- Refactor code and make it more modular
- Merging multiple methods by different input type (id, name, uri, url)
- Implement client REST API calls in a modular way.

## [0.0.1] - 2023-01-23

### Added

- Added basic function to retrieves formatted dictionary for tracks, artists and album information
- Defined function to setup the authentication and oauth2 credentials according to the Spotify API usage.
- Defined function to retrieves audio features in a well formatted form
- Implemented basic unit test
