import { Component, OnInit, Input } from '@angular/core';
import { DataService } from '../../data.service';
import { MaterializeModule } from 'angular2-materialize';
import {ApiService} from "../../share/api.service";
import {CourseTopicModel} from "../../share/course-topic-model";
import {Location} from "@angular/common";
import {Observable, Subject, Subscription} from "rxjs/index";
import {ClassModel} from "../../share/class-model";
import {UserModel} from "../../share/user-model";
import {GroupMember} from "../../share/group-member";
import { OrderPipe } from 'ngx-order-pipe';
import {ActivatedRoute, Params, Router, NavigationEnd} from '@angular/router';


@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditComponent implements OnInit {

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
  ) { 

  }

  ngOnInit() {

    const selectedClass= sessionStorage.getItem('active_group')
    if (selectedClass){

      this.apiService.LoadData(selectedClass);
      this.topicsSub=this.apiService._allTopics$; 

    }
  }

}
