import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { URLS } from 'src/environments/environment';
import { DashboardService } from './dashboard.service';
import { Season } from 'src/app/shared/interface/season.interface';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  providers: [
    DashboardService,
  ]
})
export class DashboardComponent implements OnInit {

  endpointPlayers = URLS.players;
  endpointTeams = URLS.teams;
  selectedSeason: Season = {name: '2018-19', id: 0};

  constructor(private _service: DashboardService) { }

  ngOnInit() {
    this._service.getData(URLS.seasons).subscribe(response => {
      if (response.results.length) {
        this.selectedSeason = response.results[0];
      }
    });
  }
}
