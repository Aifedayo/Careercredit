import {ActivatedRoute, Params, Router} from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { MaterializeModule } from 'angular2-materialize';
import {ApiService} from "../share/api.service";
import {CourseTopicModel} from "../share/course-topic-model";
import {Location} from "@angular/common";

@Component({
  selector: 'app-course',
  templateUrl: './course.component2.html',
  styleUrls: ['./course.component.css'],
  // providers: [MaterializeModule, CourseService],
})
export class CourseComponent implements OnInit {
  // topic: {id: number};
  public users: Array<object>  = [];
  topics = [];
  options = {};
  private  selectedTopic:number = 0;
  private  selectedGroup:number = 0;
  private videoActive:boolean=false;
  private activeTopic:CourseTopicModel;

  // constructor(
  //   public dataservice: DataService,
  //   private http: HttpClient,
  //   private courseService: CourseService,
  //   private route: ActivatedRoute) {
  //   this.dataservice.username = sessionStorage.getItem('username');
  //   this.dataservice.id = sessionStorage.getItem('id');
  //   this.dataservice.authOptions = {
  //     headers: new HttpHeaders({'Content-Type': 'application/json', 'Authorization': 'JWT ' + sessionStorage.getItem('token')})
  //   };
  //
  // }
  // all_topics=[];
  constructor(
    private apiService:ApiService,
    private route: ActivatedRoute,
    private dataservice:DataService ,
    private router:Router,
    private location:Location)
  {
    const selectedClass = + this.route.snapshot.params["group_id"];
    this.selectedGroup=selectedClass;
    if (selectedClass){
      this.apiService.LoadData(selectedClass);
      this.topics=this.apiService.CurrentTopics;
    }
  }



  ngOnInit() {
    // const selectedClass = + this.route.snapshot.params["group_id"];
    // this.selectedGroup=selectedClass
    // if (selectedClass){
    //   this.apiService.LoadData(selectedClass);
    //   this.topics=this.apiService.CurrentTopics;
    // }

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



