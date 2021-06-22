import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HeaderComponent } from './components/header/header.component';
import { HomeComponent } from './pages/home/home.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HTTP_INTERCEPTORS, HttpClient, HttpClientModule} from "@angular/common/http";
import { TwitterCardComponent } from './components/twitter-card/twitter-card.component';
import { LoginComponent } from './pages/login/login.component';
import { ChartsModule } from "ng2-charts";
import { TweetGraphComponent } from './components/tweet-graph/tweet-graph.component';
import { RegisterComponent } from './pages/register/register.component';
import {BasicAuthInterceptor} from "./helpers/BasicAuthInterceptor";
import {ErrorInterceptor} from "./helpers/ErrorInterceptor";
import { UserProfileComponent } from './pages/user-profile/user-profile.component';

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    HomeComponent,
    DashboardComponent,
    TwitterCardComponent,
    LoginComponent,
    TweetGraphComponent,
    RegisterComponent,
    UserProfileComponent,
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FontAwesomeModule,
        FormsModule,
        HttpClientModule,
        ChartsModule,
        ReactiveFormsModule,
    ],
  providers: [
    // { provide: HTTP_INTERCEPTORS, useClass: BasicAuthInterceptor, multi: true },
    // { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
