// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

export const environment = {
  production: false
};

const prefix = 'api/v1/';
export const URLS = {
  user: prefix + 'auth-user',
  login: prefix + 'api-token-auth/',
  logout: prefix + 'logout/',
  players: prefix + 'players/',
  seasons: prefix + 'seasons/',
  bet: prefix + 'teams/bet/',
  teams: prefix + 'teams/',
  hint: 'hints',
  coordinates: prefix + 'teams/coordinates/',
  admin: prefix + 'admin',
  seasonAvailable: prefix + 'seasons/available_data',
};
/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.
