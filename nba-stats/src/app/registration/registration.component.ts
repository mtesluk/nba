import { Component, OnInit, Inject } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ErrorStateMatcher } from 'src/app/shared/services/matcher';
import { RegistrationService } from './registration.service';
import { NotifyService } from '../shared/services/notify.service';
import { Router } from '@angular/router';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material';


@Component({
  selector: 'app-registrationt',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss'],
  providers: [RegistrationService],
})
export class RegistrationDialogComponent {

  matcher = new ErrorStateMatcher();
  form = new FormGroup({
    username: new FormControl(''),
    password: new FormControl(''),
    password2: new FormControl(''),
    email: new FormControl(''),
    first_name: new FormControl(''),
    last_name: new FormControl(''),
    site: new FormControl(''),
  });

  constructor(
    private _service: RegistrationService,
    private _notify: NotifyService,
    private _router: Router,
    public dialogRef: MatDialogRef<RegistrationDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {}) {}

  redirectToRegistration(): void {
    this.dialogRef.close();
    this._router.navigate(['registration']);
  }

  signUp(event) {
    const data = this.form.value;
    if (this.form.valid && data.password === data.password2) {
      delete data['password2'];
      this._service.register(data).subscribe(
        res => {
          this._notify.notify('Welcome, now log in!');
          this._router.navigate(['dashboard']);
          this.dialogRef.close();
        },
      );
    }
  }

}
