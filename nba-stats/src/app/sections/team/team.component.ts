import { Component, OnInit } from '@angular/core';
import { Season } from 'src/app/shared/interface/season.interface';
import { ActivatedRoute } from '@angular/router';
import { TeamService } from './team.service';
import { URLS } from 'src/environments/environment';

@Component({
  selector: 'app-team',
  templateUrl: './team.component.html',
  styleUrls: ['./team.component.css'],
  providers: [
    TeamService,
  ]
})
export class TeamComponent implements OnInit {

  id: string;
  seasons: Season[] = [];
  selectedSeason = 1;
  data: any;
  endpointUrl = URLS.seasons;

  constructor(private _route: ActivatedRoute,
              private _service: TeamService) { }

  ngOnInit() {
    this.id = this._route.snapshot.params['id'];
    this._service.getData(URLS.seasons).subscribe(response => {
      this.seasons = response.results;
      this.selectedSeason = this.seasons[0].id;
      this._updateSeason();
    });
  }

  _updateSeason() {
    this._service.getData(URLS.teams + this.id, {season: this.selectedSeason.toString()}).subscribe(response => {
      this.data = response;
    });
  }

  selectionChanged(event) {
    this.selectedSeason = event.value;
    this._updateSeason();
  }

}
