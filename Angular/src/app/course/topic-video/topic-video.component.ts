import { Component, OnInit } from '@angular/core';
import {ApiService} from "../../share/api.service";
import {CourseTopicModel} from "../../share/course-topic-model";
import {ActivatedRoute, Router} from "@angular/router";
import {Observable} from "rxjs/index";
import {SafePipe} from "../../share/safe.pipe";

@Component({
  selector: 'app-topic-video',
  templateUrl: './topic-video.component.html',
  styleUrls: ['./topic-video.component.css']

})
export class TopicVideoComponent implements OnInit {

  route:any ;
  public topic:any;
  public data$:any;
  constructor(private apiService:ApiService,route:ActivatedRoute,private router:Router) {
    this.route=route
  }



  ngOnInit() {

    this.data$ = this.apiService.data$
     // this.route.params.subscribe(params => {
     //    const selectedClass = + params["group_id"];
     //    if (selectedClass){
     //      this.apiService.LoadData(selectedClass);
     //    this.apiService.setActiveTopic(+params["topic_id"]);
     //      }
     //
     //    });



  }

}
