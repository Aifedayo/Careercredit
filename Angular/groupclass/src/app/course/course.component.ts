import { ActivatedRoute, Params } from '@angular/router';
import { CourseService } from './course.service';
import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MaterializeModule } from 'angular2-materialize';

@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.css'],
  providers: [MaterializeModule, CourseService],
})
export class CourseComponent implements OnInit {
  topic: {id: number};
  public users: Array<object>  = [];
  topics: any  = [];
  options = {};

  constructor(
    public dataservice: DataService,
    private http: HttpClient,
    private courseService: CourseService,
    private route: ActivatedRoute  ) {


    this.dataservice.username = sessionStorage.getItem('username');
    this.dataservice.id = sessionStorage.getItem('id');
    this.dataservice.authOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json', 'Authorization': 'JWT ' + sessionStorage.getItem('token')})
    };

  }

  ngOnInit() {
    this.dataservice.djangostudents().subscribe((data: Array<object>) => {
      this.users = data;
      console.log(data);
    });
    this.topics = this.courseService.getTopics();
    this.topic = {
      id: +this.route.snapshot.params['id']
    };
    this.route.params.subscribe((params: Params) => {
      this.topic = this.courseService.getSingleTopic(+params['id']);
    });
  }

  logout() {
    this.dataservice.logout();
  }

}



