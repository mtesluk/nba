import { Component, OnInit } from '@angular/core';
import { URLS } from 'src/environments/environment';
import { PlayersService } from './players.service';
import { Season } from 'src/app/shared/interface/season.interface';

@Component({
  selector: 'app-players',
  templateUrl: './players.component.html',
  styleUrls: ['./players.component.scss'],
  providers: [
    PlayersService,
  ]
})
export class PlayersComponent implements OnInit {
  endpointUrl: string = URLS.players;
  selectedSeason = 0;
  seasons: Season[] = [];
  filters = {};
  namesToFilter = ['name', 'age', 'position'];
  namesToSort = ['name', 'age', 'PTS', 'G'];

  constructor(private _servicePlayer: PlayersService) { }

  ngOnInit() {
    this._servicePlayer.getData(URLS.seasons).subscribe(response => {
      this.seasons = response.results;
      if (this.seasons.length) {
        this.selectedSeason = this.seasons[0].id;
      }
    });
  }
}
