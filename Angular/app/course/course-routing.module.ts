
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { Routes, RouterModule } from '@angular/router';


import { CourseComponent } from './course.component';
import { TopicChatComponent} from './topic-chat.component';
import { VideosComponent } from './videos/videos.component';
import { Video2Component } from './video2/video2.component';
import { Video3Component } from './video3/video3.component';
import { Video4Component } from './video4/video4.component';
import { Video5Component } from './video5/video5.component';
import { Video6Component } from './video6/video6.component';
import { Video7Component } from './video7/video7.component';
import { Video8Component } from './video8/video8.component';
import { Video9Component } from './video9/video9.component';
import { Video10Component } from './video10/video10.component';
import { Video11Component } from './video11/video11.component';
import { Video12Component } from './video12/video12.component';
import { Video13Component } from './video13/video13.component';
import { Video14Component } from './video14/video14.component';
import { Video15Component } from './video15/video15.component';
import { Video16Component } from './video16/video16.component';
import { Video17Component } from './video17/video17.component';
import { Video18Component } from './video18/video18.component';
import { Video19Component } from './video19/video19.component';
import { LabsComponent } from './labs/labs.component';
import {PrivateChatComponent } from './private-chat/private-chat.component';
import { TopicDetailComponent } from './topic-detail/topic-detail.component';
import { AuthGuard } from '../auth.guard';



const courseRoutes: Routes = [

    {
      path: 'classroom',
      component: CourseComponent, canActivate: [AuthGuard],

      children: [
        { path: 'topic-chat', component: TopicChatComponent },
        { path: 'videos', component: VideosComponent},
        {
          path: '',

          children: [
            { path: 'topic-detail', component: TopicDetailComponent },
            { path: 'labs', component: LabsComponent},
            { path: 'private-chat:id', component: PrivateChatComponent,
              children: [
                { path: 'id', component: PrivateChatComponent}
            ] },

            { path: 'video2', component: Video2Component},
            { path: 'video3', component: Video3Component},
            { path: 'video4', component: Video4Component},
            { path: 'video5', component: Video5Component},
            { path: 'video6', component: Video6Component},
            { path: 'video7', component: Video7Component},
            { path: 'video8', component: Video8Component},
            { path: 'video9', component: Video9Component},
            { path: 'video10', component: Video10Component},
            { path: 'video11', component: Video11Component},
            { path: 'video12', component: Video12Component},
            { path: 'video13', component: Video13Component},
            { path: 'video14', component: Video14Component},
            { path: 'video15', component: Video15Component},
            { path: 'video16', component: Video16Component},
            { path: 'video17', component: Video17Component},
            { path: 'video18', component: Video18Component},
            { path: 'video19', component: Video19Component}
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
export class CourseRoutingModule { }
