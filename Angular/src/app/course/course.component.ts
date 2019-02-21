import {ActivatedRoute, Params, Router} from '@angular/router';
import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import { DataService } from '../data.service';
import { MaterializeModule } from 'angular2-materialize';
import {ApiService} from "../share/api.service";
import {CourseTopicModel} from "../share/course-topic-model";
import {Location} from "@angular/common";
import {Observable, Subject, Subscription} from "rxjs/index";
import {ClassModel} from "../share/class-model";
import {UserModel} from "../share/user-model";
import {GroupMember} from "../share/group-member";
import { OrderPipe } from 'ngx-order-pipe';

@Component({
  selector: 'app-course',
  templateUrl: './course.component2.html',
  styleUrls: ['./course.component.css'],
  providers: [MaterializeModule],
})
export class CourseComponent implements OnInit {
  items: ClassModel[];
  topicsSub:any;
  classes: Observable<ClassModel[]>;
  topics = [];
  public  selectedTopic:number = 0;
  username:string;
  private  selectedGroup:number = 0;
  // public groupMembers$: Observable<UserModel[]>;
  public groupMembers$: Observable<GroupMember[]>;
  public noOfUsers$:Observable<any>;

  constructor(
    private apiService:ApiService,
    private route: ActivatedRoute,
    public dataservice:DataService ,
    private router:Router,
    private location:Location,
    private cdr:ChangeDetectorRef)

  {
    this.username=sessionStorage.getItem('username');

  }

  ngOnInit() {
    this.route.params.subscribe(params=> {

    this.classes=this.apiService.getAvailableClasses();
    const selectedClass = + params["group_id"];
    this.selectedGroup=selectedClass;
    if (selectedClass){
      const selectedTopic = + params["topic_id"];
      this.apiService.LoadData(selectedClass);
      this.topicsSub=this.apiService._allTopics$;


      this.groupMembers$ = this.apiService.getGroupMembers(selectedClass);
      this.noOfUsers$ = this.apiService.getMembers(selectedClass);


    }if(this.selectedTopic){
        this.setTopic(this.selectedTopic)
      }
    })

  }

  public setTopic(id){
    this.selectedTopic=id;
    this.apiService.setActiveTopic(id);
    this.goToVideo();
  }

  reset(){

  }
  countUsers(){
    this.groupMembers$.subscribe(d=>{

   console.log(d)
    })
    let c = 0;
    return c;
  }
  goToVideo(){
    this.reset();
        this.apiService.setActiveTopic(this.selectedTopic);
    this.router.navigate([ '/classroom/'+ this.selectedGroup +'/topic/'+this.selectedTopic+''])
  }
  goToLab(id){
    this.reset();
    this.apiService.setActiveTopic(this.selectedTopic);
    this.router.navigate([ '/classroom/'+ this.selectedGroup +'/topic/'+this.selectedTopic+'/lab'])
  }
  goToNote(){
    this.reset();
    this.apiService.setActiveTopic(this.selectedTopic);
    this.router.navigate([ '/classroom/'+ this.selectedGroup +'/topic/'+this.selectedTopic+'/notes'])
  }
  goToChat(){
    this.reset();
    this.router.navigate([this.location.path()+'topic/'+this.selectedTopic+'/chat'])
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



