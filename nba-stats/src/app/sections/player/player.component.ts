import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PlayerService } from './player.service';
import { URLS } from 'src/environments/environment';
import { Season } from 'src/app/shared/interface/season.interface';

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css'],
  providers: [
    PlayerService
  ]
})
export class PlayerComponent implements OnInit {

  id: string;
  seasons: Season[] = [];
  selectedSeason = 1;
  data: any;
  endpointUrl = URLS.seasons;

  constructor(private _route: ActivatedRoute,
              private _service: PlayerService) { }

  ngOnInit() {
    this.id = this._route.snapshot.params['id'];
    this._service.getData(URLS.seasons).subscribe(response => {
      this.seasons = response.results;
      this.selectedSeason = this.seasons.length > 0 ? this.seasons[0].id : this.selectedSeason;
      this._updateSeason();
    });
  }

  _updateSeason() {
    this._service.getData(URLS.players + this.id, {season: this.selectedSeason.toString()}).subscribe(response => {
      this.data = response;
    });
  }

  selectionChanged(event) {
    this.selectedSeason = event.value;
    this._updateSeason();
  }

}
