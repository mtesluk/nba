import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { MatSnackBar } from '@angular/material';

@Injectable({
  providedIn: 'root'
})
export class NotifyService {

  private notify$ = new Subject<string>();

  constructor(private _snackBar: MatSnackBar) {
    this.notify$.subscribe(message => {
      this._snackBar.open(message, 'OK', {
        duration: 5000,
        panelClass: ['snackbar'],
        horizontalPosition: 'right',
        verticalPosition: 'bottom',
      });
    });
  }

  notify(message) {
    this.notify$.next(message);
  }
}
