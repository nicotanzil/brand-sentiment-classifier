import {Injectable} from "@angular/core";
import {HttpHandler, HttpInterceptor, HttpRequest, HttpEvent} from "@angular/common/http";
import {AuthenticationService} from "../services/authentication.service";
import {Observable} from "rxjs";

@Injectable()
export class BasicAuthInterceptor implements HttpInterceptor {
  constructor(private authenticationService: AuthenticationService) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // add authorization header with basic auth credentials if available
    const encoded = btoa(req.body.username + ":" + req.body.password);
    const currentUser = this.authenticationService.currentUserValue;
    currentUser.token = encoded;
    if(currentUser && currentUser.token) {
      req = req.clone({
        setHeaders: {
          Authorization: `Basic ${currentUser.token}`,
        }
      });
    }
    return next.handle(req);
  }
}
