import { DataService } from './../data.service';
import { Course2Component } from './course2.component';
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule} from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatVideoModule } from 'mat-video';
import { CourseChatComponent } from './course-chat/course-chat.component';
import { Course2RoutingModule } from './course2-routing.module';
import { MaterializeModule } from 'angular2-materialize';


@NgModule({
  imports: [
    BrowserAnimationsModule,
    MatVideoModule,
    BrowserModule,
    CommonModule,
    Course2RoutingModule,
    MaterializeModule,
    DataService
  ],
  declarations: [
    Course2Component,
    CourseChatComponent,
  ],
  providers: [],
  bootstrap: [Course2Component]
})
export class Course2Module { }
