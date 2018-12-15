import {ActivatedRoute, Params, Router} from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { MaterializeModule } from 'angular2-materialize';
import {ApiService} from "../share/api.service";
import {CourseTopicModel} from "../share/course-topic-model";
import {Location} from "@angular/common";
import {Observable, Subscription} from "rxjs/index";
import {ClassModel} from "../share/class-model";

@Component({
  selector: 'app-course',
  templateUrl: './course.component2.html',
  styleUrls: ['./course.component.css'],
  // providers: [MaterializeModule, CourseService],
})
export class CourseComponent implements OnInit {
  items: ClassModel[];
  classes: Observable<ClassModel[]>;
  public users: Array<object>  = [];
  topics = [];
  options = {};
  private  selectedTopic:number = 0;
  private  selectedGroup:number = 0;
  private videoActive:boolean=false;
  public activeTopic:CourseTopicModel;

  constructor(
    private apiService:ApiService,
    private route: ActivatedRoute,
    public dataservice:DataService ,
    private router:Router,
    private location:Location)
  {
    const selectedClass = + this.route.snapshot.params["group_id"];
    const selectedTopic = + this.route.snapshot.params["topic_id"];
    this.selectedGroup=selectedClass;
    if (selectedClass){
      this.apiService.LoadData(selectedClass);
      this.topics=this.apiService.CurrentTopics;
      console.log(this.apiService.getUsers(selectedClass))
    }
    if(this.selectedTopic){
      this.setTopic(selectedTopic)
    }
  }



  ngOnInit() {
    this.classes=this.apiService.getAvailableClasses();
  }

  public setTopic(id){
    this.selectedTopic=id;
    this.apiService.setActiveTopic(id);
    this.activeTopic=this.apiService.getActiveTopic();
    this.goToVideo();
  }

  reset(){
     this.videoActive=false;

  }
  goToVideo(){
    this.reset();
    this.router.navigate([ '/classroom/'+ this.selectedGroup +'/topic/'+this.activeTopic.id+''])
  }
  goToLab(){
    this.reset();
    this.apiService.setActiveTopic(this.selectedTopic);
    this.activeTopic=this.apiService.getActiveTopic();
    this.router.navigate([ '/classroom/'+ this.selectedGroup +'/topic/'+this.activeTopic.id+'/lab'])
  }
  goToNote(){
    this.reset();
    this.apiService.setActiveTopic(this.selectedTopic);
    this.activeTopic=this.apiService.getActiveTopic();
    this.router.navigate([ '/classroom/'+ this.selectedGroup +'/topic/'+this.activeTopic.id+'/notes'])
  }
  goToChat(){
    this.reset();
    this.router.navigate([this.location.path()+'topic/'+this.activeTopic.id+'/chat'])
  }

  getTopic(id: number) {
  const topic = this.topics.find(
    (data) => {
      return data.id === id;
    }
  );
  return topic;
}
  logout() {
    this.dataservice.logout();
  }

}



