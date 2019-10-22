import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { InfoResponse } from 'src/app/shared/interface/response.interface';


@Injectable()
export class AdminActionDialogService {

  constructor(private _http: HttpClient) { }

  getData(endpointUrl: string, filters?: {[name: string]: string}): Observable<[]> {
    return this._http.get<[]>(endpointUrl, {params: {...filters}});
  }

  postData(endpointUrl: string, data: {[name: string]: string | number}, filters?: {[name: string]: string}): Observable<InfoResponse> {
    return this._http.post<InfoResponse>(endpointUrl, data, {params: {...filters}});
  }
}