import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DashboardRoutingModule } from './dashboard-routing.module';
import { HeaderComponent } from './header/header.component';
import { ContentComponent } from './content/content.component';
import { ProfileComponent } from './profile/profile.component';
import { AttendanceComponent } from './attendance/attendance.component';
import { StudentsComponent } from './students/students.component';
import { SettingsComponent } from './settings/settings.component';
import {ListComponent} from './list/list.component'
import {FormsModule} from "@angular/forms";

@NgModule({
  imports: [
    CommonModule,
    DashboardRoutingModule,
    FormsModule
  ],
  declarations: [HeaderComponent, ContentComponent, ProfileComponent, AttendanceComponent, StudentsComponent, SettingsComponent,ListComponent]
})
export class DashboardModule { }
