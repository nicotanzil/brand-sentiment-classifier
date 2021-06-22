import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {map} from "rxjs/operators";
import {BehaviorSubject, Observable} from "rxjs";
import {User} from "../models/user";

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  private currentUserSubject!: BehaviorSubject<User>;
  public currentUser!: Observable<User>;

  constructor(private http: HttpClient) {
    this.currentUserSubject = new BehaviorSubject(JSON.parse(<string>localStorage.getItem('token')));
    this.currentUser = this.currentUserSubject.asObservable()
  }

  public get currentUserValue(): User {
    return this.currentUserSubject.value;
  }

  isLoggedIn() {
    return false
  }

  login(username: string, password: string) {
    return this.http.post(`${environment.apiUrl}/login`, {username: username, password: password})
      .pipe(map(token => {
        // store the jwt token in local storage to keep user logged in between page refreshes
        localStorage.setItem('token', JSON.stringify(token));
        if (token instanceof User) {
          this.currentUserSubject.next(token);
        }
      }));
  }

  logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('token');
    // @ts-ignore
    this.currentUserSubject.next(null);
  }
}
