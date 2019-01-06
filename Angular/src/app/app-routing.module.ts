
import { LinuxComponent } from './linux/linux.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { SignupComponent} from './signup/signup.component';
import { LoginComponent } from './login/login.component';
import { CourseComponent } from './course/course.component';
import { AuthGuard } from './auth.guard';





const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full'},
  { path: 'classroom', component: CourseComponent, canActivate: [AuthGuard]},
  { path: 'linux', component: LinuxComponent, canActivate: [AuthGuard]},
  { path: 'signup', component: SignupComponent },
  { path: 'login', component: LoginComponent },
  { path: 'home', component: HomeComponent},
  { path: 'unauthorised', component: LoginComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AppRoutingModule { }
