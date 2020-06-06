import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AdminDashboardComponent } from './admin-dashboard.component';
import { StudentsComponent } from './students/students.component';
import { StatusComponent } from './status/status.component';
import { EditComponent } from './edit/edit.component';
import { EditDetailsComponent } from './edit-details/edit-details.component';

const routes: Routes = [
  { path: 'admin', component: AdminDashboardComponent, 
    children:[
      {path:'students',component:StudentsComponent,
        children:[{path: 'status/:user_id', component: StatusComponent}]
      },
      {path:'edit', component:EditComponent,
        children:[{path: 'topic/:topic_id', component: EditDetailsComponent}]
      },    
    ]
  },

];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminDashboardRoutingModule { }
