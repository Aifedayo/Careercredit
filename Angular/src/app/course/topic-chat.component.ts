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


      // getting a reference to the overall list, which is the parent container of the list items
  @ViewChild(MatList, { read: ElementRef }) matList: ElementRef;

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
    // this.avatar=environment.API_URL + `media/avatar.png`;
    this.avatar=this.dataService.profileImgIsSet()?
      environment.API_URL + sessionStorage.getItem('profile_img'):
      environment.API_URL + `media/avatar.png`;
    this.websocket = new WebSocket(environment.WS_URL+"?token="+this.token);
    this.activeGroup = sessionStorage.getItem('active_group');
   }

  ngOnInit() {
    this.callWebsocket()
  }

  sendMessage(message,type:string) {
     if(this.dataService.profileImgIsSet()){
       if (message!==""){
         const now = new Date();
         const context = {
           action:'sendMessage',
           active_group:this.activeGroup,
           user:sessionStorage.getItem('username'),
           content:message,
           the_type:type,
           timestamp:now.toLocaleDateString(),
           token:this.token
         };

         this.websocket.send(
            JSON.stringify(context)
          );
          this.chat_text = '';
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
                  const url=environment.API_URL + data['url'];
                  this.sendMessage(url,data['type'])
                },
                error => console.log( error)
            );
      }
  }

  ngAfterViewInit(): void {
    this.mutableObserver();
  }

  callWebsocket(){
    this.websocket.onopen = (evt) => {
      const now=new Date();
      const context ={
        action:'getRecentMessages',
        active_group:this.activeGroup,
        token:this.token
      };
      // console.log(context)
      this.websocket.send(JSON.stringify(context));
    };

    this.websocket.onmessage = (evt) => {
      // console.log(evt.data);
      const data = JSON.parse(evt.data);
      if(data['active_group'] == this.activeGroup){
        if (data['messages'] !== undefined) {
          data['messages'].forEach((message)=>{
              const messg = {
                user:message.user.username,
                profile_img:message.user.profile_img,
                content:message.content,
                the_type:message.the_type,
                timestamp:message.timestamp,
              };
              
              this.messages.push(messg);
            }
          );
        }
      }
    };

  }

  mutableObserver(){
    this.mutationObserver = new MutationObserver((mutations) => {
        this.scrollToBottom();
      }
    );

    this.mutationObserver.observe(this.matList.nativeElement, {
        childList: true
    });
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

  // auto-scroll fix: inspired by this stack overflow post
  // https://stackoverflow.com/questions/35232731/angular2-scroll-to-bottom-chat-style
  private scrollToBottom(){
    try {
      this.matList.nativeElement.scrollTop = 
      this.matList.nativeElement.scrollHeight;
      const chat_scroll = document.getElementById('chat_div_space');
      chat_scroll.scrollTop = chat_scroll.scrollHeight;
    } catch (err) {}
  }

}
