export interface Stat {
    [name: string]: number;
}

export interface Player {
    id: number;
    name: string;
    age: string;
    position: string;
    stats: Stat[];
}
