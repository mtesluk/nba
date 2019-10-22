import { Component, OnInit, Inject } from '@angular/core';
import { AuthService } from '../shared/services/auth.service';
import { Router } from '@angular/router';
import { NotifyService } from '../shared/services/notify.service';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialog } from '@angular/material';
import { RegistrationDialogComponent } from '../registration/registration.component';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginDialogComponent {

  username: string;
  password: string;

  constructor(private _auth: AuthService,
    private _router: Router,
    private _notifyService: NotifyService,
    public dialog: MatDialog,
    public dialogRef: MatDialogRef<LoginDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {}) {}

  redirectToRegistration(): void {
    this.dialogRef.close();
    this.dialog.open(RegistrationDialogComponent, {
      width: '20vw',
    });
  }

  onSubmit() {
    this._auth.login(this.username, this.password).subscribe(response => {
      this.dialogRef.close();
      this._notifyService.notify('Logged in');
      this._router.navigate(['dashboard']);
    },
    error => {
      this._notifyService.notify('Wrong credentials');
    });
  }
}
