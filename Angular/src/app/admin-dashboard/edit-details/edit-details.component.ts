import { Component, OnInit } from '@angular/core';
import {environment} from "../../../environments/environment";
import {ApiService} from "../../share/api.service";
import {UserModel} from "../../share/user-model";
// import * as $ from 'jquery';
import { DataService } from 'src/app/data.service';
// import processHelper from './process.helper'
import {CourseTopicModel} from "../../share/course-topic-model";
import {ActivatedRoute, Router} from "@angular/router";
import {EditTopicModel} from "../../share/course-topic-model";


@Component({
  selector: 'app-edit-details',
  templateUrl: './edit-details.component.html',
  styleUrls: ['./edit-details.component.css']
})
export class EditDetailsComponent implements OnInit {
  public topic = new CourseTopicModel();
  topicsSub: any;
  private topics 
  constructor(
    private apiService:ApiService, 
    private dataService:DataService,
    private router:Router,
    private route:ActivatedRoute
  ) { }

  ngOnInit() {
    this.route.params.subscribe(data=>{
      const selectedClass= sessionStorage.getItem('active_group')
      if (selectedClass){
        // console.log(typeof(data['topic_id']))
        this.apiService.LoadData(selectedClass);
        // console.log(this.apiService.allTopics)
        this.topicsSub=this.apiService._allTopics$;
        this.topicsSub.subscribe(res=>{
          this.topics = res
          // console.log(this.topics)
          this.topics.forEach(element => {
            if (data['topic_id']==element.id){
              this.topic.topic = element.topic
              this.topic.video= element.video
              this.topic.id = element.id
            }
            
          });
          
        })
        // console.log('this.topics')
        
      }
    });
  }

  editTopic(){
    const selectedClass= sessionStorage.getItem('active_group')
    this.apiService.editTopic(selectedClass, this.topic).subscribe(res=>{
      this.topic.topic = this.topic.topic
      this.topic.video = this.topic.video
    })
  }

}
