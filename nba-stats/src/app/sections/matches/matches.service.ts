import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Response } from 'src/app/shared/interface/response.interface';


@Injectable()
export class MatchService {

  constructor(private _http: HttpClient) { }

  getData(endpointUrl: string, filters?: {[name: string]: string}): Observable<Response> {
    return this._http.get<Response>(endpointUrl, {params: {...filters}});
  }
}
