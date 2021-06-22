import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class AppService {

  baseURL: string = "http://127.0.0.1:5000/"

  constructor(private http: HttpClient) { }

  getByKeyword(keyword: string): Observable<any> {
    console.log(keyword)
    return this.http.get(`${environment.apiUrl}/keyword/${keyword}`);
  }

  getByUser(keyword: string): Observable<any> {
    console.log(keyword);
    return this.http.get(`${environment.apiUrl}/user/${keyword}`);
  }

}
