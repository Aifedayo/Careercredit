import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AdminDashboardComponent } from './admin-dashboard.component';
import { StudentsComponent } from './students/students.component';
import { StatusComponent } from './status/status.component';


const routes: Routes = [
  { path: 'admin', component: AdminDashboardComponent, 
    children:[
      {path:'students',component:StudentsComponent,
        children:[{path: 'status/:user_id', component: StatusComponent}]},
    ]
  },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminDashboardRoutingModule { }
