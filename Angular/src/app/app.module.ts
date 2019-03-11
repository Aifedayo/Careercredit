import { CourseService } from './course/course.service';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatVideoModule } from 'mat-video';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { TopicChatComponent } from './course/topic-chat.component';
import { CourseComponent } from './course/course.component';
import { MaterializeModule } from 'angular2-materialize';
import { CourseRoutingModule } from './course/course-routing.module';
import { AppRoutingModule } from './app-routing.module';
import { PrivateChatComponent } from './course/private-chat/private-chat.component';
import {DataService} from './data.service';
import {Location} from "@angular/common";
import {CourseModule} from "./course/course.module";
import {ApiService} from "./share/api.service";
import { SafePipe } from './share/safe.pipe';
import {OrderModule} from "ngx-order-pipe";
import {DashboardModule} from "./dashboard/dashboard.module";

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    PrivateChatComponent,

  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,



    BrowserAnimationsModule,
    MatVideoModule,
    MaterializeModule,
    AppRoutingModule,
    CourseModule,
    OrderModule,
    DashboardModule

  ],
  providers: [DataService,Location,ApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
