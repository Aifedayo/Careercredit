import { Component, OnInit } from '@angular/core';
import { DataService } from '../../data.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-course-chat',
  templateUrl: './course-chat.component.html',
  styleUrls: ['./course-chat.component.css']
})
export class CourseChatComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

}
