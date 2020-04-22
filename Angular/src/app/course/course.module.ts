import { MaterializeModule } from 'angular2-materialize';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule} from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterModule } from '@angular/router';
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
import { MentionModule } from './_mention/mention.module';
import {OthersChatComponent} from './others-chat/others-chat.component';
import {MyChatComponent} from './my-chat/my-chat.component';
import {QouteMessageComponent} from './qoute-message/qoute-message.component';

@NgModule({
  imports: [
    BrowserAnimationsModule,
    RouterModule,
    MatVideoModule,
    BrowserModule,
    CommonModule,
    CourseRoutingModule,
    FormsModule,
    OrderModule,
    SharedModule,
    AlertModule,
    LightboxModule,
    MentionModule,
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
    OthersChatComponent,
    MyChatComponent,
    QouteMessageComponent,
  ],
  providers: [AuthGuard,VerificationGuard],
  bootstrap: [CourseComponent]
})
export class CourseModule { }
