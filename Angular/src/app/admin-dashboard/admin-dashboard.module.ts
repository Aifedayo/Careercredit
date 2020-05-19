import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {DashboardModule} from "../dashboard/dashboard.module";
import { AdminDashboardRoutingModule } from './admin-dashboard-routing.module';
import { RouterModule } from '@angular/router'
import { HeaderComponent } from './header/header.component';
import { StudentsComponent } from './students/students.component';
import { AdminDashboardComponent } from './admin-dashboard.component';

@NgModule({
  imports: [
    CommonModule,
    AdminDashboardRoutingModule, 
    RouterModule

  ],
  declarations: [HeaderComponent,StudentsComponent, AdminDashboardComponent],
  bootstrap: [ AdminDashboardComponent ]
})
export class AdminDashboardModule { }
