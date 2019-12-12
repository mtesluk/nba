import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { AuthService } from 'src/app/shared/services/auth.service';
import { MatDialog } from '@angular/material';
import { LoginDialogComponent } from 'src/app/login/login.component';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit {

  @Output() public sidenavToggle = new EventEmitter();
  get user() {
    return this._auth.getUserUsername();
  }
  get user_credits() {
    return this._auth.getUserCredits();
  }
  constructor(
    private _auth: AuthService,
    public dialog: MatDialog,
  ) { }

  ngOnInit() {
  }

  isAuthenticated() {
    return this._auth.isAuthenticated();
  }

  isAdmin() {
    return this._auth.isAdmin();
  }

  logout() {
    return this._auth.logout();
  }

  openDialog(): void {
    this.dialog.open(LoginDialogComponent, {
      backdropClass: 'dialog-background',
      width: '20vw',
    });
  }

  onToggleSidenav = () => {
    this.sidenavToggle.emit();
  }
}
