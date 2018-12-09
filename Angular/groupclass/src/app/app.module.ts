import { CourseService } from './course/course.service';
import { TopicDetailComponent } from './course/topic-detail/topic-detail.component';
import { LinuxChatComponent } from './linux/linux-chat/linux-chat.component';
import { LinuxRoutingModule } from './linux/linux-routing.module';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatVideoModule } from 'mat-video';
import { AppComponent } from './app.component';
import { SignupComponent } from './signup/signup.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { TopicChatComponent } from './course/topic-chat.component';
import { CourseComponent } from './course/course.component';
import { MaterializeModule } from 'angular2-materialize';
import { CourseRoutingModule } from './course/course-routing.module';
import { AppRoutingModule } from './app-routing.module';
import { PrivateChatComponent } from './course/private-chat/private-chat.component';
import { Course2Component } from './course2/course2.component';
import { LinuxComponent } from './linux/linux.component';
import {DataService} from './data.service';
import {Location} from "@angular/common";
import {TopicVideoComponent} from "./course/topic-video/topic-video.component";
import {TopicLabComponent} from "./course/topic-lab/topic-lab.component";
import {TopicNotesComponent} from "./course/topic-notes/topic-notes.component";
import {CourseModule} from "./course/course.module";




@NgModule({
  declarations: [

    AppComponent,
    LinuxChatComponent,
    LinuxComponent,
    SignupComponent,
    HomeComponent,
    LoginComponent,
    // CourseComponent,
    PrivateChatComponent,
    Course2Component,
    // TopicChatComponent,
    // TopicDetailComponent,
    // TopicVideoComponent,
    // TopicLabComponent,
    // TopicNotesComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    BrowserAnimationsModule,
    MatVideoModule,
    MaterializeModule,
    LinuxRoutingModule,
    // CourseRoutingModule,
    AppRoutingModule,
    CourseModule
  ],
  providers: [DataService,Location ],
  bootstrap: [AppComponent]
})
export class AppModule { }
