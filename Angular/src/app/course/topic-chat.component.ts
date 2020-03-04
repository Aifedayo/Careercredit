import {Component, ElementRef, OnInit,  ViewChild} from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient } from '@angular/common/http';

import {ApiService} from "../share/api.service";
import {ChatMessage} from "../share/chat-message";
import {Observable} from "rxjs/index";
import {MatList} from "@angular/material";
import {environment} from "../../environments/environment";
import {UserModel} from "../share/user-model";
import { AlertService } from './_alert/alert.service';

export enum TYPE {Plain='plain', Image='image', File='file'}

@Component({
  selector: 'app-topic-chat',
  templateUrl: './topic-chat.component2.html',
  styleUrls: ['./topic-chat.component.css']
})




export class TopicChatComponent implements OnInit {

  private mutationObserver: MutationObserver;
  private activeGroup:string;

  public current_user:string;
  public users: Array<object> = [];
  public chat_text  = '';
  public messages = [];
  public the_message:ChatMessage;
  public websocket;
  public email;
  public type=TYPE;
  public avatar:string;
  private token:string;
  public offset_id:Number = 0;
  private is_send_message:Boolean = false;
  private recent_message_is_set:Boolean = false;


  // getting a reference to the overall list, which is the parent container of the list items
  @ViewChild(MatList, { read: ElementRef }) matList: ElementRef;
  @ViewChild('ChatSpace') chatSpace: ElementRef<HTMLElement>;

  private user$: Observable<UserModel>;
  public environment = environment;
  
  constructor(
    private http: HttpClient, 
    private apiService:ApiService,
    private alertService: AlertService,
    private dataService: DataService,
  ) {
      this.token = sessionStorage.getItem('token');
      this.user$=this.apiService.getUserInfo();
      this.current_user = sessionStorage.getItem('username');
      this.activeGroup = sessionStorage.getItem('active_group');
      this.setProfileImage();
   }

  ngOnInit() {
    this.callWebsocket()
  }

  sendMessage(message,type:string) {
     if(this.dataService.profileImgIsSet()){
       if(message!==""){
          const now = new Date();
          const context = {
            action:'sendMessage',
            active_group:this.activeGroup,
            user:sessionStorage.getItem('username'),
            content:message,
            the_type:type,
            timestamp:this.onlyHsMs(now.toLocaleTimeString()),
            token:this.token
          };  

          this.websocket.send(JSON.stringify(context));
          this.chat_text = '';
          this.is_send_message = true
        } 
        //console.log(message)
      }
      else{
          this.alertService.error(
            'You need to set your profile image to continue'
          );
      }
  }

  openImage(url):void{} 

  fileChange(event): void {
      const fileList: FileList = event.target.files;
      if (fileList.length > 0) {
          const file = fileList[0];

          const formData = new FormData();
          formData.append('file', file, file.name);

          this.apiService.uploadFile(formData)
            .subscribe(
                data => {
                  // const url=environment.API_URL + data['url'];
                  this.sendMessage(data['url'],data['type'])
                },
                error => console.log( error)
            );
      }
  }

  ngAfterViewInit(): void {
    this.mutableObserver();
  }

  callWebsocket(){
    this.websocket = new WebSocket(
      environment.WS_URL+"?token="+this.token
    );

    this.websocket.onopen = (evt) => {
      if(!this.recent_message_is_set){
        this.getMessages()
      }
    };

    this.websocket.onmessage = (evt) => {
      const data = JSON.parse(evt.data);
      console.log(data)
      this.processMessages(data)
    };

    this.websocket.onclose = ()=>{
        // this.websocket = null
        console.log('... trying reconnection in 5 sec....')
        setTimeout(this.callWebsocket,5000)
    }
  }


  getProfileImg(proImgUrl:string){
    var image_url = "";
      if(
        proImgUrl.startsWith("https://") || 
        proImgUrl.startsWith("http://") 
      ){
        image_url =  proImgUrl
      }
      else {
        image_url = environment.API_URL + proImgUrl
      }
    return image_url
  }

  getMessages(){
    if(this.offset_id != -1){
      const data = {
        active_group:this.activeGroup,
        offset_id:this.offset_id,
        token:this.token
      };

      this.apiService.getMessages(data).subscribe(
          data => {
            this.is_send_message = false
            if(this.offset_id != 0) data['is_next']=true
            this.processMessages(data)
            this.offset_id = data['next_offset_id']
            this.recent_message_is_set = true
          },
          error => console.log( error)
      );
    }
  }

  isOthers(username){
    return username !== this.current_user && 
    username !== 'DATE-INFO'
  }

  formatDate(that_day) {
      const date = new Date(that_day)
      const today = new Date
      const yesterday = new Date 
      let format_date = date.toLocaleDateString(
        'en-US',{weekday:'long',month:'long',day:'numeric'}
      )
      yesterday.setDate(today.getDate() - 1)
      if(date.toLocaleDateString() == today.toLocaleDateString()){
        format_date = 'Today'
      }else if (date.toLocaleDateString() == yesterday.toLocaleDateString()){
        format_date = 'Yesterday'
      }
      return format_date
  }

  private processMessages(data){
    if(data['active_group'] == this.activeGroup){
      if (data['messages'] !== undefined) {    
        if(data['is_next']){
          this.messages = [...data['messages'],...this.messages]
          this.chatSpace.nativeElement.scrollTop = 100
        }
        else if(data['from_where'] === 'send'){
          this.messages = [...this.messages,...data['messages']]
          this.is_send_message = true
        }else{
          this.messages = data['messages']
          this.is_send_message = true
        }
      }
    }
  }

  // auto-scroll fix: inspired by this stack overflow post
  // https://stackoverflow.com/questions/35232731/angular2-scroll-to-bottom-chat-style
  private scrollToBottom(){
    try {
      this.chatSpace.nativeElement.scrollTop = 
      this.chatSpace.nativeElement.scrollHeight
      this.matList.nativeElement.scrollTop = 
      this.matList.nativeElement.scrollHeight;
    } catch (err) {}
  }

  private mutableObserver(){
    this.mutationObserver = new MutationObserver((mutations) => {
        if(this.is_send_message) this.scrollToBottom();
      }
    );

    this.mutationObserver.observe(this.matList.nativeElement, {
        childList: true
    });
  }

  private setProfileImage(){
    // this.avatar=environment.API_URL + `media/avatar.png`;
    this.avatar=this.dataService.profileImgIsSet()?
    environment.API_URL + sessionStorage.getItem('profile_img'):
    environment.API_URL + `media/avatar.png`;
  }

  private onlyHsMs(time){
    time = time.split(':')
    let ampm = time.pop()
    ampm = ampm.split(' ')
    return `${time[0]}:${time[1]} ${ampm[1]}`
  }
}
