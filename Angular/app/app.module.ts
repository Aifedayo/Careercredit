import { TopicDetailComponent } from './course/topic-detail/topic-detail.component';
import { LinuxChatComponent } from './linux/linux-chat/linux-chat.component';
import { LinuxRoutingModule } from './linux/linux-routing.module';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { FileSelectDirective } from 'ng2-file-upload';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatVideoModule } from 'mat-video';
import { AppComponent } from './app.component';
import { SignupComponent } from './signup/signup.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { VideosComponent } from './course/videos/videos.component';
import { Video2Component } from './course/video2/video2.component';
import { Video3Component } from './course/video3/video3.component';
import { Video4Component } from './course/video4/video4.component';
import { Video5Component } from './course/video5/video5.component';
import { Video6Component } from './course/video6/video6.component';
import { Video7Component } from './course/video7/video7.component';
import { Video8Component } from './course/video8/video8.component';
import { Video9Component } from './course/video9/video9.component';
import { Video10Component } from './course/video10/video10.component';
import { Video11Component } from './course/video11/video11.component';
import { LabsComponent } from './course/labs/labs.component';
import { TopicChatComponent } from './course/topic-chat.component';
import { CourseComponent } from './course/course.component';
import { MaterializeModule } from 'angular2-materialize';
import { CourseRoutingModule } from './course/course-routing.module';
import { AppRoutingModule } from './app-routing.module';
import { Video12Component } from './course/video12/video12.component';
import { Video13Component } from './course/video13/video13.component';
import { Video14Component } from './course/video14/video14.component';
import { Video15Component } from './course/video15/video15.component';
import { Video16Component } from './course/video16/video16.component';
import { Video17Component } from './course/video17/video17.component';
import { Video18Component } from './course/video18/video18.component';
import { Video19Component } from './course/video19/video19.component';
import { PrivateChatComponent } from './course/private-chat/private-chat.component';
import { Course2Component } from './course2/course2.component';
import { LinuxComponent } from './linux/linux.component';




@NgModule({
  declarations: [

    AppComponent,
    FileSelectDirective,
    LinuxChatComponent,
    LinuxComponent,
    SignupComponent,
    HomeComponent,
    LoginComponent,
    CourseComponent,
    VideosComponent,
    Video2Component,
    Video3Component,
    LabsComponent,
    TopicChatComponent,
    Video4Component,
    Video5Component,
    Video6Component,
    Video7Component,
    Video8Component,
    Video9Component,
    Video10Component,
    Video11Component,
    Video12Component,
    Video13Component,
    Video14Component,
    Video15Component,
    Video16Component,
    Video17Component,
    Video18Component,
    Video19Component,
    PrivateChatComponent,
    Course2Component,
    TopicDetailComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    BrowserAnimationsModule,
    MatVideoModule,
    MaterializeModule,
    LinuxRoutingModule,
    CourseRoutingModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
