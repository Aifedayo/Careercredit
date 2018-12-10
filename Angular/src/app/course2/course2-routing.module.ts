import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { Routes, RouterModule } from '@angular/router';


import { Course2Component } from './course2.component';
import { CourseChatComponent} from './course-chat/course-chat.component';

import { AuthGuard } from '../auth.guard';



const courseRoutes: Routes = [

    {
      path: 'course2',
      component: Course2Component, canActivate: [AuthGuard],
      children: [
        {
          path: '',

          children: [

            { path: 'course-chat', component: CourseChatComponent },
          ]
        }
      ]
    }
  ];
@NgModule({
  imports: [
    BrowserModule,
    RouterModule.forChild(courseRoutes),
  ],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class Course2RoutingModule { }
