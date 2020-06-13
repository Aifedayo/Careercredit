import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "../../environments/environment";
import {CourseTopicModel} from "./course-topic-model";
import {ActivatedRoute} from "@angular/router";
import {Location} from "@angular/common";
import {Observable, of,from, ReplaySubject,BehaviorSubject, Subject} from "rxjs/index";
import {Topic} from "../course/topic.model";
import {ClassModel} from "./class-model";
import {UserModel} from "./user-model";
import {GroupMember} from "./group-member";
import {AttendanceModel} from "./attendance-model";
import {EditTopicModel} from "./course-topic-model";
import { filter, flatMap, tap } from 'rxjs/operators';
import { CometChat } from "@cometchat-pro/chat"

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  CurrentClasses = [];
  private tt;
  private sharedTopic;
  public CurrentTopics = [];
  private allTopics = new Subject();
  _allTopics$ = this.allTopics.asObservable();
  private _data = new Subject();
  data$ = this._data.asObservable();
  private _users = new Subject();
  users$ = this._users.asObservable();


  private headers: HttpHeaders = new HttpHeaders();
  private fileheaders: HttpHeaders = new HttpHeaders();


  constructor(private httpClient: HttpClient, location: Location, route: ActivatedRoute) {
    this.headers = this.headers.append('Accept', 'application/json');
    this.headers = this.headers.append('Authorization', 'Token ' + sessionStorage.getItem('token'));
    this.fileheaders = this.fileheaders.append('Authorization', 'Token ' + sessionStorage.getItem('token'));
    this._allTopics$.subscribe(res => {
      this.tt = res
    })
  }

  refreshToken() {

    this.headers = new HttpHeaders();
    this.fileheaders = new HttpHeaders();
    this.headers = this.headers.append('Accept', 'application/json');
    this.headers = this.headers.append('Authorization', 'Token ' + sessionStorage.getItem('token'));
    this.fileheaders = this.fileheaders.append('Authorization', 'Token ' + sessionStorage.getItem('token'));

  }

  setActiveTopic(id) {
    this._data.next(this.getTopic(id))
  }

  getActiveTopic() {
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

  LoadData(selectedClass) {
    this.getCourseDetails(selectedClass)
      .subscribe(res => {
        res['topics'].forEach(entry => {
          let topic = new CourseTopicModel();
          topic.id = entry.id;
          topic.note = entry.note;
          topic.topic = entry.topic;
          topic.video = entry.video;
          topic.tasks = entry.tasks;
          this.CurrentTopics.push(topic);
        });
        this.allTopics.next(this.CurrentTopics);
        this.CurrentTopics = []
      });

  }
 
  getCourseDetails(id) {
    this.refreshToken()
    return this.httpClient.get(environment.API_URL + `sso_api/group/` + id, {headers: this.headers})
  }

  getAvailableClasses(): Observable<ClassModel[]> {
    this.refreshToken()
    return this.httpClient.get<ClassModel[]>(environment.API_URL + `sso_api/groups`, {headers: this.headers})
  }

  getGroupMembers(group_id): Observable<GroupMember[]> {
    this.refreshToken()
    // this.httpClient.get<UserModel[]>(environment.API_URL + `sso_api/group/`+group_id+`/users`,{headers:this.headers}).subscribe(data=>{
    // })

    return this.httpClient.get<GroupMember[]>(environment.API_URL + `sso_api/group/` + group_id + `/users`, {headers: this.headers})
  }

  getMembers(group_id): Observable<UserModel[]> {
    this.refreshToken()
    return this.httpClient.get<UserModel[]>(environment.API_URL + `sso_api/group/` + group_id + `/users2`, {headers: this.headers})
    // return this.httpClient.get<GroupMember[]>(environment.API_URL + `sso_api/group/`+group_id+`/users`,{headers:this.headers})
  }

  uploadFile(data) {
    this.refreshToken()
    let head = new HttpHeaders();
    head = head.append('Authorization', 'Token e973d9bef2d8464bb84cdc06af35fd4a76a37b90')
    // return this.httpClient.put( 'http://localhost:8000/sso_api/upload',data,{headers:this.fileheaders})
    return this.httpClient.put(environment.API_URL + 'sso_api/upload', data, {headers: this.fileheaders})
  }

  getUserAttendance(group_id, user_id = null) {
    if (user_id === null) {
      return this.httpClient.get<AttendanceModel>(environment.API_URL + `sso_api/group/` + group_id + `/userlog`, {headers: this.headers})
      // return this.httpClient.get(environment.API_URL + `sso_api/group/`+group_id+`/userlog`,{headers:this.headers})

    }
    return this.httpClient.get<AttendanceModel>(environment.API_URL + `sso_api/group/` + group_id + `/userlog/` + user_id, {headers: this.headers})
    // return this.httpClient.get<AttendanceModel[]>(environment.API_URL + `sso_api/group/`+group_id+`/userlog/`+user_id,{headers:this.headers})


  }

  getUserInfo(user_id = null) {
    this.refreshToken()
    if (user_id === null) {
      return this.httpClient.get<UserModel>(environment.API_URL + `sso_api/user/`, {headers: this.headers})
    }
    return this.httpClient.get<UserModel>(environment.API_URL + `sso_api/user/` + user_id, {headers: this.headers})


  }

  getGroupInfo(group_id) {
    this.refreshToken()
    return this.httpClient.get<ClassModel>(environment.API_URL + `sso_api/group/` + group_id + `/detail`, {headers: this.headers})
  }

  uploadImage(data) {
    this.refreshToken()
    let head = new HttpHeaders();
    head = head.append('Authorization', 'Token e973d9bef2d8464bb84cdc06af35fd4a76a37b90');
    // return this.httpClient.put( 'http://localhost:8000/sso_api/upload',data,{headers:this.fileheaders})
    return this.httpClient.put(environment.API_URL + 'sso_api/user/upload', data, {headers: this.fileheaders})
  }

  uploadVideo(data) {
    this.refreshToken()
    let head = new HttpHeaders();
    head = head.append('Authorization', 'Token e973d9bef2d8464bb84cdc06af35fd4a76a37b90');
    // return this.httpClient.put( 'http://localhost:8000/sso_api/upload',data,{headers:this.fileheaders})
    return this.httpClient.put(environment.API_URL + 'sso_api/user/upload', data, {headers: this.fileheaders})
  }


  updateUserInfo(obj: UserModel) {
    this.refreshToken()
    let head = new HttpHeaders();
    head = this.headers;
    head = head.append('Content-Type', 'application/json');
    const x = {'first_name': obj.first_name, 'last_name': obj.last_name};
    return this.httpClient.post(environment.API_URL + 'sso_api/user/', JSON.stringify(x), {headers: head})
  }

  updateGroupInfo(obj: ClassModel) {
    this.refreshToken()
    let head = new HttpHeaders();
    head = this.headers;
    head = head.append('Content-Type', 'application/json');
    const x = {'video_required': obj.video_required};
    return this.httpClient.post(environment.API_URL + 'sso_api/group/' + obj.id + `/detail`, JSON.stringify(x),
    {headers: head})
  }

  getUserVerification(){

  }


   videoUploded(group_id) {
    this.refreshToken();
    this.httpClient.get(environment.API_URL + `sso_api/group/` + group_id
      + `/user/verification`, {headers: this.headers}).subscribe(res=>{
        return !! res['uploaded']
    });
    return false
  }

   videoRequired(group_id){
        this.refreshToken();
     this.httpClient.get<ClassModel>(environment.API_URL + `sso_api/group/` + group_id + `/detail`, {headers: this.headers})
  .subscribe(res=>{
      return !! res['video_required']
    });
     return false
  }


  getLabs(topic_id){
    this.refreshToken();
    return this.httpClient.get<UserModel>(environment.API_URL + `sso_api/topic/` + topic_id+ `/labs`, {headers: this.headers})

  }

  getNotes(topic_id){
    this.refreshToken();
    return this.httpClient.get<UserModel>(environment.API_URL + `sso_api/topic/` + topic_id+ `/note`, {headers: this.headers})

  }

  //Chat Api
  getMessages(data){
    this.refreshToken();
    let head = this.headers;
    head = head.append('Content-Type', 'application/json');
    const url =`${environment.API_URL}awsgateway/get_messages/`
    return this.httpClient.post(
      url,JSON.stringify(data), {headers: head}
    )
  }

  getMentionUsers(data):Observable<any[]>{
    this.refreshToken();
    let head = this.headers;
    head = head.append('Content-Type', 'application/json');
    const url =`${environment.API_URL}awsgateway/get_mention_users/`
    return this.httpClient.post<any[]>(
      url,JSON.stringify(data), {headers: head}
    )
  }

  deleteUser(group_id, obj){
    this.refreshToken()
    let head = new HttpHeaders();
    head = this.headers;
    head = head.append('Content-Type', 'application/json');
    let data = {"id": obj}
    let url = environment.API_URL + `sso_api/group/${group_id}/deleted`
    console.log(JSON.stringify(data))
    console.log(url)
    // return this.httpClient.put( 'http://localhost:8000/sso_api/upload',data,{headers:this.fileheaders})
    return this.httpClient.put(environment.API_URL + `sso_api/group/${group_id}/deleted`, JSON.stringify(data),
    {headers: head})
  }

  editTopic(group_id, obj:CourseTopicModel){
    this.refreshToken()
    let head = new HttpHeaders();
    head = this.headers;
    head = head.append('Content-Type', 'application/json');
    let data = {"id": obj.id, "topic":obj.topic, "video":obj.video}
    console.log(JSON.stringify(data))
    // return this.httpClient.put( 'http://localhost:8000/sso_api/upload',data,{headers:this.fileheaders})
    return this.httpClient.put(environment.API_URL + `sso_api/group/${group_id}`, JSON.stringify(data),
    {headers: head})
  }

  
}

