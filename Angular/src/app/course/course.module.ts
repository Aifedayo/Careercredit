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
import { TopicLabComponent } from './topic-lab/topic-lab.component';
import { TopicNotesComponent } from './topic-notes/topic-notes.component';
import { TopicVideoComponent } from './topic-video/topic-video.component';
import {FormsModule} from "@angular/forms";
import {SafePipe} from "../share/safe.pipe";

@NgModule({
  imports: [
    BrowserAnimationsModule,
    MatVideoModule,
    BrowserModule,
    CommonModule,
    CourseRoutingModule,
    FormsModule,

  ],
  declarations: [
    CourseComponent,
    TopicChatComponent,
    TopicLabComponent,
    TopicNotesComponent,
    TopicVideoComponent,
    SafePipe
  ],
  providers: [],
  bootstrap: [CourseComponent]
})
export class CourseModule { }
