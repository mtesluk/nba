import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler, HttpEvent } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { ActivatedRoute } from '@angular/router';


@Injectable()
export class AuthInterceptor implements HttpInterceptor {
    constructor(
        private _auth: AuthService,
        private _route: ActivatedRoute) {}

    intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        req = req.clone({setHeaders: {Authorization: (this._auth.getToken() ? 'JWT ' + this._auth.getToken() : '')}});
        return next.handle(req);
    }
}
