export const environment = {
  production: true
};

const prefix = 'api/v1/';
export const URLS = {
  user: prefix + 'auth-user',
  login: prefix + 'api-token-auth/',
  logout: prefix + 'logout/',
  players: prefix + 'players/',
  seasons: prefix + 'seasons/',
  matches: prefix + 'matches/',
  match_stats: prefix + 'match_stats',
  teams: prefix + 'teams/',
  hint: 'hints',
  coordinates: prefix + 'teams/coordinates/',
  admin: prefix + 'admin',
  seasonAvailable: prefix + 'seasons/available_data',
};