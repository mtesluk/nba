import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material';
import { AdminActionDialogComponent } from 'src/app/shared/components/admin-action-dialog/admin-action-dialog.component';
import { Router } from '@angular/router';


@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent implements OnInit {

  constructor(
    private _router: Router,
    public dialog: MatDialog,
  ) { }

  ngOnInit() {
  }

  openDialog(type: string, choices: boolean, seasonsDb: boolean): void {
    this.dialog.open(AdminActionDialogComponent, {
      backdropClass: 'dialog-background',
      width: '20vw',
      data: {type, choices, seasonsDb}
    });
  }

  goAdmin() {
    this._router.navigate(['/admin']);
  }

}
