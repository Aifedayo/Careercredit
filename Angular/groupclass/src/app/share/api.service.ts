import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {CourseTopicModel} from "./course-topic-model";
import {ActivatedRoute} from "@angular/router";
import {Location} from "@angular/common";
import {Observable, of, Subject} from "rxjs/index";
import {Topic} from "../course/topic.model";

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private sharedTopic;
  public AllClasses=[];
  public ActiveClass:number;
  public CurrentTopics=[];
  public ActiveTopic:number;
  private _data = new Subject();
  data$ = this._data.asObservable();


  private headers: HttpHeaders = new HttpHeaders();
  constructor(private httpClient:HttpClient,location:Location,route:ActivatedRoute) {
    this.headers=this.headers.append('Accept', 'application/json');
    this.headers=this.headers.append('Authorization', 'Token ' + sessionStorage.getItem('token'));



  }

  emitTopic(){}

   setActiveTopic(id){
    this.sharedTopic=this.getTopic(id)
     this.set()
  }
    set() {
    this._data.next(this.sharedTopic);
  }
  getActiveTopic(){
     return this.sharedTopic
  }
  getactiveTopic(): Observable<Topic> {
  return of(this.sharedTopic);
}
  getTopic(id: number) {
  return this.CurrentTopics.find(
    (data) => {
      return data.id === id;
    }
  )


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
      });
  }
  getCourseDetails(id){
    return this.httpClient.get(environment.API_URL + `sso_api/group/` + id,{headers:this.headers})
  }
  getAvailableClasses(){
    return this.httpClient.get(environment.API_URL + `sso_api/groups/`,{headers:this.headers})
  }
}
