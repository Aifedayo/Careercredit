import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ContentComponent} from "./content/content.component";
import {ProfileComponent} from "./profile/profile.component";
import {AuthGuard} from "../auth.guard";
import {AdminGuard} from "./admin.guard";
import {StudentsComponent} from "./students/students.component";
import {AttendanceComponent} from "./attendance/attendance.component";
import {SettingsComponent} from "./settings/settings.component";

const routes: Routes = [
  {path:'dashboard',component:ContentComponent,canActivate:[AuthGuard],
    children:[
      {path:'profile',component:ProfileComponent},
      {path:'settings',component:SettingsComponent, canActivate:[AdminGuard]},
      {path:'attendance',component:AttendanceComponent, canActivate:[AdminGuard]},
      {path:'students',component:StudentsComponent,
        children:[
        {path:'attendance/:user_id',component:AttendanceComponent, canActivate:[AdminGuard]},
      ]},




  ]

  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})

export class DashboardRoutingModule { }
