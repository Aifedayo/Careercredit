import { CourseService } from './course.service';

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { Routes, RouterModule } from '@angular/router';
import { CourseComponent } from './course.component';
import { TopicChatComponent} from './topic-chat.component';
import {PrivateChatComponent } from './private-chat/private-chat.component';
import { AuthGuard } from '../auth.guard';
import {TopicVideoComponent} from "./topic-video/topic-video.component";
import {TopicLabComponent} from "./topic-lab/topic-lab.component";
import {TopicNotesComponent} from "./topic-notes/topic-notes.component";



const courseRoutes: Routes = [

    {
      path: 'classroom/:group_id',
      component: CourseComponent, canActivate: [AuthGuard],
      children: [
        { path: 'topic-chat', component: TopicChatComponent },
        { path: 'topic/:topic_id', component: TopicVideoComponent},
        { path: 'topic/:topic_id/video', component: TopicVideoComponent},
        { path: 'topic/:topic_id/lab', component: TopicLabComponent},
        { path: 'topic/:topic_id/notes', component: TopicNotesComponent},
        { path: 'private-chat', component: PrivateChatComponent,
          children: [
          { path: ':id', component: PrivateChatComponent},
        ]},
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
