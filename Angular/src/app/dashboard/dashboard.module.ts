import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router'
import { DashboardRoutingModule } from './dashboard-routing.module';
import { HeaderComponent } from './header/header.component';
import { ContentComponent } from './content/content.component';
import { ProfileComponent } from './profile/profile.component';
import { AttendanceComponent } from './attendance/attendance.component';
import { StudentsComponent } from './students/students.component';
import { SettingsComponent } from './settings/settings.component';
import {ListComponent} from './list/list.component';
import {FormsModule} from "@angular/forms";
import { AlertModule } from './../course/_alert/alert.module';


@NgModule({
  imports: [
    CommonModule,
    DashboardRoutingModule,
    FormsModule,
    RouterModule,
    AlertModule
  ],
  declarations: [HeaderComponent, ContentComponent, ProfileComponent, AttendanceComponent, StudentsComponent, SettingsComponent,ListComponent],
  bootstrap: [ HeaderComponent ]
})
export class DashboardModule { }
