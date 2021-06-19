import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AppService {

  baseURL: string = "http://127.0.0.1:5000/"

  constructor(private http: HttpClient) { }

  getByKeyword(keyword: string): Observable<any> {
    console.log(keyword)
    return this.http.get(this.baseURL + 'keyword/' + keyword);
  }
}
