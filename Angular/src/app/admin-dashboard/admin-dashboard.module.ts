import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {DashboardModule} from "../dashboard/dashboard.module";
import { AdminDashboardRoutingModule } from './admin-dashboard-routing.module';
import { RouterModule } from '@angular/router'
import { HeaderComponent } from './header/header.component';
import { StudentsComponent } from './students/students.component';
import { AdminDashboardComponent } from './admin-dashboard.component';
import { StatusComponent } from './status/status.component';
import { EditComponent } from './edit/edit.component';
import { EditDetailsComponent } from './edit-details/edit-details.component';
import {FormsModule} from "@angular/forms";

@NgModule({
  imports: [
    CommonModule,
    AdminDashboardRoutingModule, 
    RouterModule,
    FormsModule,

  ],
  declarations: [HeaderComponent,StudentsComponent, AdminDashboardComponent, StatusComponent, EditComponent, EditDetailsComponent],
  bootstrap: [ AdminDashboardComponent ]
})
export class AdminDashboardModule { }
