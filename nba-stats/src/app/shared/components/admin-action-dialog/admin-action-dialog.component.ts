import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialog } from '@angular/material';
import { URLS } from 'src/environments/environment';
import { Season } from 'src/app/shared/interface/season.interface';
import { AdminActionDialogService } from './admin-action-dialog.service';
import { NotifyService } from 'src/app/shared/services/notify.service';

const SEASON_TYPE_MAPPER: {[name: string]: string} = {RS: 'Regular Season'};

@Component({
  selector: 'app-admin-action-dialog',
  templateUrl: './admin-action-dialog.component.html',
  styleUrls: ['./admin-action-dialog.component.scss'],
  providers: [
    AdminActionDialogService,
  ]
})
export class AdminActionDialogComponent implements OnInit {
  get seasonTypes() {
    return Object.values(SEASON_TYPE_MAPPER);
  }
  endpointUrl: string = URLS.teams;
  seasons: string[] = ['2019-20', '2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14', '2012-13', '2011-12', '2010-11'];
  choices: string[] = ['Players and team stats', 'Matches'];
  selectedChoice: string = this.choices[0];
  selectedSeason: string = this.seasons[0];
  selectedSeasonType: string = this.seasonTypes[0];

  constructor(
    private _notificationService: NotifyService,
    private _service: AdminActionDialogService,
    public dialog: MatDialog,
    public dialogRef: MatDialogRef<AdminActionDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {type: string, choices: boolean, seasonsDb: boolean}
  ) {}

  ngOnInit() {
    if (this.data.seasonsDb) {
      this._service.getData(URLS.seasonAvailable).subscribe(response => {
        this.seasons = response;
      });
    }
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  confirm() {
    this._service.postData(
      URLS.admin,
      {type: this.data.type, secondary_type: this.selectedChoice, season: this.selectedSeason, season_type: this.selectedSeasonType},
      {}
    ).subscribe((response: {message: string}) => {
      this._notificationService.notify(response.message);
      this.dialogRef.close();
    });
  }

}
