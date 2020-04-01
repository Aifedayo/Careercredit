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
import {OrderModule} from "ngx-order-pipe";
import {SharedModule} from "../../shared/shared.module";
import { VerificationComponent } from './verification/verification.component';
import {AuthGuard} from "../auth.guard";
import {VerificationGuard} from "../verification.guard";
import { CourseListComponent } from './course-list/course-list.component';
import { AlertModule } from './_alert/alert.module';
import { LightboxModule } from './_lightbox/lightbox.module';
import { ImageLightboxComponent } from './_image-lightbox/image-lightbox.component';
import { InfiniteScrollComponent } from './_infinite-scroll/Infinite-scroll.component';
import { RouterModule } from '@angular/router';

@NgModule({
  imports: [
    BrowserAnimationsModule,
    MatVideoModule,
    BrowserModule,
    CommonModule,
    CourseRoutingModule,
    FormsModule,
    OrderModule,
    SharedModule,
    AlertModule,
    LightboxModule,
    RouterModule

  ],
  declarations: [
    CourseComponent,
    TopicChatComponent,
    TopicLabComponent,
    TopicNotesComponent,
    TopicVideoComponent,
    SafePipe,
    VerificationComponent,
    CourseListComponent,
    ImageLightboxComponent,
    InfiniteScrollComponent,
  ],
  providers: [AuthGuard,VerificationGuard],
  bootstrap: [CourseComponent]
})
export class CourseModule { }
