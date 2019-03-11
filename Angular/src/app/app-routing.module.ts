
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { CourseComponent } from './course/course.component';
import { AuthGuard } from './auth.guard';
import {ContentComponent} from "./dashboard/content/content.component";
import {VerificationComponent} from "./course/verification/verification.component";





const routes: Routes = [
  { path: '', redirectTo: '/classroom', pathMatch: 'full'},
  { path: 'classroom', component: CourseComponent, canActivate: [AuthGuard]},
  { path: 'dashboard', component: ContentComponent },
  { path: 'home', component: HomeComponent},
  { path: 'v', component: VerificationComponent},
];



@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AppRoutingModule { }
