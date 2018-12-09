import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {ApiService} from "../../share/api.service";

@Component({
  selector: 'app-topic-notes',
  templateUrl: './topic-notes.component.html',
  styleUrls: ['./topic-notes.component.css']
})
export class TopicNotesComponent implements OnInit {

 route:any ;
  public topic:any = null;
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
    })
  }
  ngOnInit() {
  }

}
