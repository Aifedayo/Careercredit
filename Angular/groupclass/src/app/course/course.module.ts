import { TopicDetailComponent } from './topic-detail/topic-detail.component';
import { MaterializeModule } from 'angular2-materialize';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule} from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatVideoModule } from 'mat-video';
import { CourseComponent } from './course.component';
import { TopicChatComponent } from './topic-chat.component';
import { CourseService } from './course.service';
import { CourseRoutingModule } from './course-routing.module';
import { TopicListComponent } from './topic-list/topic-list.component';
import { TopicLabComponent } from './topic-lab/topic-lab.component';
import { TopicNotesComponent } from './topic-notes/topic-notes.component';
import { TopicVideoComponent } from './topic-video/topic-video.component';
import {FormsModule} from "@angular/forms";

@NgModule({
  imports: [
    BrowserAnimationsModule,
    MatVideoModule,
    BrowserModule,
    CommonModule,
    CourseRoutingModule,
    MaterializeModule,
    FormsModule
  ],
  declarations: [
    CourseComponent,
    TopicChatComponent,
    TopicDetailComponent,
    TopicListComponent,
    TopicLabComponent,
    TopicNotesComponent,
    TopicVideoComponent
  ],
  providers: [CourseService],
  bootstrap: [CourseComponent]
})
export class CourseModule { }
