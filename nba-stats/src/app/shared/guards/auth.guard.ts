import { Injectable } from '@angular/core';
import { Router, ActivatedRouteSnapshot, RouterStateSnapshot, CanActivate } from '@angular/router';
import { AuthService } from 'src/app/shared/services/auth.service';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { NotifyService } from 'src/app/shared/services/notify.service';


@Injectable()
export class AuthGuard implements CanActivate {

  constructor(
    private _router: Router,
    private _auth: AuthService,
    private _notification: NotifyService,
  ) { }

  isPermAdmin(permissionLevel: string) {
    return permissionLevel === 'admin';
  }

  isAdmin(permissionLevel: string) {
    return this.isPermAdmin(permissionLevel) ? (this._auth.isAdmin() ? true : false) : true;
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> | boolean {
    const permissionLevel = route.data.level;
    if ([undefined, null].includes(permissionLevel)) {
      return true;
    }

    if (this._auth.isAuthenticated()) {
      return this.isAdmin(permissionLevel);
    } else {
      return this._auth.shouldBeAuthenticated().pipe(
        map((result) => {
          if (result === false) {
            this._router.navigate(['dashboard']);
          }
          if (!this.isAdmin(permissionLevel)) {
            this._router.navigate(['dashboard']);
            this._notification.notify('You are not admin');
            return false;
          }
          return result;
        }),
        catchError( err => {
          if (err.status === 401) {
            this._notification.notify(
              this.isPermAdmin(permissionLevel) ? 'You are not admin' : 'You are not allowed to access that part, please sign in'
            );
          }
          this._auth.logout();
          return of(false);
        })
      );
    }
  }

}
