import { Component, OnInit } from '@angular/core';
import { URLS } from 'src/environments/environment';
import { MatchService } from './matches.service';
import { Season } from 'src/app/shared/interface/season.interface';

@Component({
  selector: 'app-matches',
  templateUrl: './matches.component.html',
  styleUrls: ['./matches.component.scss'],
  providers: [
    MatchService,
  ]
})
export class MatchesComponent implements OnInit {
  endpointUrl: string = URLS.matches;
  selectedSeason = 0;
  seasons: Season[] = [];
  descOrder = '-date';
  filters = {};
  namesToFilter = ['season_type', 'date', 'team_host', 'team_visitor'];

  constructor(private _service: MatchService) { }

  ngOnInit() {
    this._service.getData(URLS.seasons).subscribe(response => {
      this.seasons = response.results;
      this.selectedSeason = this.seasons[0].id;
    });
  }
}
