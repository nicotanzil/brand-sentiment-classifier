import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {DashboardComponent} from "./pages/dashboard/dashboard.component";
import {HomeComponent} from "./pages/home/home.component";
import {LoginComponent} from "./pages/login/login.component";
import {AuthGuard} from "./guards/auth.guard";
import {UserProfileComponent} from "./pages/user-profile/user-profile.component";

const routes: Routes = [
  {
    path: 'dashboard/:keyword',
    component: DashboardComponent,
    // canActivate: [AuthGuard]
  },
  {
    path: 'user/:keyword',
    component: UserProfileComponent,
  },
  {
    path: 'login',
    component: LoginComponent,
  },
  {
    path: '',
    component: HomeComponent,
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
