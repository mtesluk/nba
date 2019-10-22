import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { URLS } from 'src/environments/environment';
import { Observable } from 'rxjs';
import { User } from 'src/app/shared/interface/user.interface';


@Injectable()
export class RegistrationService {

  constructor(private _http: HttpClient) { }

  register(data: User): Observable<User> {
    return this._http.post<User>(URLS.user, data);
  }

}
