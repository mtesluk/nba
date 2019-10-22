import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { MatchService } from './match.service';
import { URLS } from 'src/environments/environment';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-match',
  templateUrl: './match.component.html',
  styleUrls: ['./match.component.css'],
  providers: [
    MatchService
  ]
})
export class MatchComponent implements OnInit {

  id: string;
  data: any;
  teamHost: string;
  teamVisitor: string;
  stats: string [];
  hostStats: string [];
  visitorStats: string [];
  arrayHost: any;
  arrayVisitor: any;
  displayedColumns: string [];
  headers: string[];
  length: number;
  toDisplay: [{}] = [{}];

  constructor(private _route: ActivatedRoute,
              private _service: MatchService) {}

  ngOnInit() {
    this.id = this._route.snapshot.params['id'];
    this._setup();
  }

  _setup() {
    this._service.getData(URLS.matches + this.id).subscribe(response => {
      this.data = response;
      this.teamHost = response['team_host'];
      this.teamVisitor = response['team_visitor'];
      this.arrayHost = response['stats'][0]['team_host_stats'];
      this.arrayVisitor = response['stats'][0]['team_visitor_stats'];
      this.stats = Object.keys(this.arrayHost);
      this.hostStats = Object.values(this.arrayHost);
      this.visitorStats = Object.values(this.arrayVisitor);
      this.length = this.visitorStats.length;
      this.displayedColumns = ['stats', 'teamHost', 'teamVisitor'];
      for (let i = 0 ; i < this.length ; i++) {
        this.toDisplay.push({stats: this.stats[i], hostStats: this.hostStats[i], visitorStats: this.visitorStats[i]});
      }
      this.toDisplay.shift();
    });
  }

}
