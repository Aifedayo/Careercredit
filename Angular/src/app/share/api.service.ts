import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {CourseTopicModel} from "./course-topic-model";
import {ActivatedRoute} from "@angular/router";
import {Location} from "@angular/common";
import {Observable, of, Subject} from "rxjs/index";
import {Topic} from "../course/topic.model";
import {ClassModel} from "./class-model";
import {UserModel} from "./user-model";

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  CurrentClasses=[];
  private tt;
  private sharedTopic;
  public CurrentTopics=[];
  private allTopics= new Subject();
  _allTopics$=this.allTopics.asObservable();
  private _data = new Subject();
  data$ = this._data.asObservable();
  private _users=new Subject();
  users$ = this._users.asObservable();


  private headers: HttpHeaders = new HttpHeaders();
  constructor(private httpClient:HttpClient,location:Location,route:ActivatedRoute) {
    this.headers=this.headers.append('Accept', 'application/json');
    this.headers=this.headers.append('Authorization', 'Token ' + sessionStorage.getItem('token'));
    this._allTopics$.subscribe(res=>{
      this.tt=res
    })
  }
   setActiveTopic(id){
     this._data.next(this.getTopic(id))
  }
  getActiveTopic(){
     return this.sharedTopic
  }
  getTopic(id: number) {
     return this.tt.find(
    (data) => {
      return data.id === id;
    }
  )

}
  getUsers(id: number) {
   const _class = this.CurrentClasses.find(
    (data) => {
      return data.id === id;
    }
  );
    return _class
}
  LoadData(selectedClass){
    this.getCourseDetails(selectedClass)
          .subscribe(res=>{
        res['topics'].forEach(entry=>{
          let topic = new CourseTopicModel();
        topic.id=entry.id;
        topic.note= entry.note;
        topic.topic=entry.topic;
        topic.video=entry.video;
        topic.tasks=entry.tasks;
        this.CurrentTopics.push(topic);
        })
            this.allTopics.next(this.CurrentTopics);
        this.CurrentTopics=[]
      });

  }
  getCourseDetails(id){
    return this.httpClient.get(environment.API_URL + `sso_api/group/` + id,{headers:this.headers})
  }
  getAvailableClasses():Observable<ClassModel[]>{
    return this.httpClient.get<ClassModel[]>(environment.API_URL + `sso_api/groups`,{headers:this.headers})
  }
  getGroupMembers(group_id):Observable<UserModel[]>{
    return this.httpClient.get<UserModel[]>(environment.API_URL + `sso_api/group/`+group_id+`/users`,{headers:this.headers})
  }

}
