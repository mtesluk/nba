export interface Stat {
  [name: string]: number;
}

export interface MatchStat {
  id: number;
  team: string;
  match: string;
  stats: Stat[];
}
