import {ActivatedRoute, Params, Router, NavigationEnd} from '@angular/router';
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
  course:ClassModel;
  // public chatTab;
  // public videoTab;
  topicsSub:any;
  classes: Observable<ClassModel[]>;
  topics = [];
  public  selectedTopic:number = 0;
  username:string;
  public  selectedGroup:number = 0;
  currentUrl : string;

  // public groupMembers$: Observable<UserModel[]>;
  public groupMembers$: Observable<GroupMember[]>;
  public noOfUsers$:Observable<any>;
  public group$: Observable<ClassModel>;
  public is_instructor:boolean; 

  constructor(
    private apiService:ApiService,
    private route: ActivatedRoute,
    public dataservice:DataService ,
    private router:Router,
    private location:Location,
)

  {
    this.username=sessionStorage.getItem('username');
    this.currentUrl = ''
  }

  ngOnInit() {
    this.route.params.subscribe(params=> {
      this.classes=this.apiService.getAvailableClasses();
      const selectedClass = + params["group_id"];
      sessionStorage.setItem('active_group', selectedClass.toString() );
      this.group$ = this.apiService.getGroupInfo(sessionStorage.getItem('active_group'))
      this.selectedGroup=selectedClass;
      if (selectedClass){
        const selectedTopic = + params["topic_id"];
        
        this.apiService.LoadData(selectedClass);
        this.topicsSub=this.apiService._allTopics$;

        this.noOfUsers$ = this.apiService.getMembers(selectedClass);        
      }

      if(this.selectedTopic){
          this.setTopic(this.selectedTopic)
      }
    })

    this.router.events.subscribe((event) => {
        if(event instanceof NavigationEnd){
          this.currentUrl = event.url;
        }
    });

    this.groupMembers$ = this.apiService.getGroupMembers(
      sessionStorage.getItem('active_group')
    );
    this.is_instructor = this.dataservice.isInstructor(
    );
    console.log(this.dataservice.isInstructor())

  }

  ngAfterViewInit(){
    if(!this.selectedTopic){
      this.topicsSub.subscribe(topics => {
        sessionStorage.setItem('active_topic',topics[0].id);
        this.selectedTopic=topics[0].id;
        this.apiService.setActiveTopic(topics[0].id);
        this.currentUrl = '/classroom/'+ this.selectedGroup +'/topic/'+topics[0].id;
      });
    }
  }

  public setTopic(id){
    sessionStorage.setItem('active_topic',id);
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

  goToVideo(end=''){
    this.reset();
    this.apiService.setActiveTopic(this.selectedTopic);
    this.router.navigate([ '/classroom/'+ this.selectedGroup +'/topic/'+this.selectedTopic+end])
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

  tabToVideo(id){
    sessionStorage.setItem('active_topic',id);
    this.selectedTopic=id;
    this.apiService.setActiveTopic(id);
    this.goToVideo('/video');
  }

  isCureentTab(tab){
    return this.currentUrl.indexOf(tab) !== -1;
  }

  isCurrentRoute(topic_id): boolean {
    const path  = '/classroom/'+ this.selectedGroup +'/topic/'+topic_id;
    return path === this.currentUrl || 
    path+'/video' === this.currentUrl ||
    path+'/lab' === this.currentUrl ||
    path+'/notes' === this.currentUrl;
  } 

}



