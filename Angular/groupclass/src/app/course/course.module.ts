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
import { VideosComponent } from './videos/videos.component';
import { LabsComponent } from './labs/labs.component';






@NgModule({
  imports: [
    BrowserAnimationsModule,
    MatVideoModule,
    BrowserModule,
    CommonModule,
    CourseRoutingModule,
    MaterializeModule,
  ],
  declarations: [
    CourseComponent,
    TopicChatComponent,
    VideosComponent,
    LabsComponent,
    TopicDetailComponent
  ],
  providers: [CourseService],
  bootstrap: [CourseComponent]
})
export class CourseModule { }
