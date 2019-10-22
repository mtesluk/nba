import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material';
import { AdminActionDialogComponent } from 'src/app/shared/components/admin-action-dialog/admin-action-dialog.component';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent implements OnInit {

  constructor(
    public dialog: MatDialog,
  ) { }

  ngOnInit() {
  }

  openDialog(type: string, choices: boolean, seasonsDb: boolean): void {
    this.dialog.open(AdminActionDialogComponent, {data: {type, choices, seasonsDb}});
  }

}
