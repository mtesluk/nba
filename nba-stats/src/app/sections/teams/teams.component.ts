import { Component, OnInit } from '@angular/core';
import { URLS } from 'src/environments/environment';
import { Season } from 'src/app/shared/interface/season.interface';
import { TeamsService } from './teams.service';

@Component({
  selector: 'app-teams',
  templateUrl: './teams.component.html',
  styleUrls: ['./teams.component.scss'],
  providers: [
    TeamsService,
  ]
})
export class TeamsComponent implements OnInit {
  endpointUrl: string = URLS.teams;
  selectedSeason = 0;
  seasons: Season[] = [];
  filters = {};
  namesToFilter = ['name'];
  namesToSort = ['name', 'PTS'];

  constructor(private _service: TeamsService) { }

  ngOnInit() {
    this._service.getData(URLS.seasons).subscribe(response => {
      this.seasons = response.results;
      if (this.seasons.length) {
        this.selectedSeason = this.seasons[0].id;
      }
    });
  }
}
