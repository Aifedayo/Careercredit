import { Component, OnInit } from '@angular/core';
import {ApiService} from "../../share/api.service";
import {ActivatedRoute, Router} from "@angular/router";
import {Observable} from "rxjs/index";

@Component({
  selector: 'app-topic-lab',
  templateUrl: './topic-lab.component.html',
  styleUrls: ['./topic-lab.component.css']
})
export class TopicLabComponent implements OnInit {
  route:any ;
  public topic:any = null;
  public _task:Observable<any>=null;
  constructor(private apiService:ApiService,route:ActivatedRoute,private router:Router) {
    this.route=route;
        this.route.params.subscribe(params => {
      const selectedClass = + params["group_id"];
    if (selectedClass){
      this.apiService.LoadData(selectedClass);
    this.apiService.setActiveTopic(+params["topic_id"]);
       }
        });
    this.topic = this.apiService.getActiveTopic();
        this.apiService.data$.subscribe(data=>{
      this.topic=data;
      console.log(this.topic)
      this._task= this.apiService.data$
    })
  }
  ngOnInit() {
  }

}
