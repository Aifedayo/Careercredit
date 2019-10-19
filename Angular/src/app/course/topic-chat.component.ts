import {Component, ElementRef, OnInit, QueryList, ViewChild, ViewChildren} from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient } from '@angular/common/http';

import {ApiService} from "../share/api.service";
import {ChatMessage} from "../share/chat-message";
import {Observable} from "rxjs/index";
import {MatList, MatListItem} from "@angular/material";
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

  public current_user:string;
  public users: Array<object> = [];
  public chat_text  = '';
  public messages = [];
  public the_message:ChatMessage;
  public websocket;
  public email;
  public type=TYPE;
  public avatar:string ;

      // getting a reference to the overall list, which is the parent container of the list items
  @ViewChild(MatList, { read: ElementRef }) matList: ElementRef;

  // getting a reference to the items/messages within the list
  @ViewChildren(MatListItem, { read: ElementRef }) matListItems: QueryList<MatListItem>;
  private user$: Observable<UserModel>;
  public environment = environment;
  
  constructor(
    private http: HttpClient, 
    private apiService:ApiService,
    private alertService: AlertService,
    private dataService: DataService,
  ) {

    this.user$=this.apiService.getUserInfo();
    this.current_user = sessionStorage.getItem('username');
    // this.avatar=environment.API_URL + `media/avatar.png`;
    this.avatar=this.dataService.profileImgIsSet()?
      environment.API_URL + sessionStorage.getItem('profile_img'):
      environment.API_URL + `media/avatar.png`;
    this.websocket = new WebSocket(environment.WS_URL);
    this.websocket.onopen = (evt) => {
      const now=new Date();
      const m= new ChatMessage();
      m.user=sessionStorage.getItem('username');
      m.the_type = 'plain';
      m.message="!join Djangoclass";
      m.timestamp= now.toString();
      this.websocket.send(JSON.stringify(m));
      };

      this.websocket.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        if (data['messages'] !== undefined) {
            for (let i = 0; i < data['messages']['length']; i++) {
              this.the_message=new ChatMessage();
              this.the_message.user = data['messages'][i]['user'];
              this.the_message.message = data['messages'][i]['message'];
              this.the_message.timestamp = data['messages'][i]['timestamp'];
              this.the_message.the_type = data['messages'][i]['the_type'];
              this.messages.push(this.the_message);
              const chat_scroll = document.getElementById('chat_div_space');
              chat_scroll.scrollTop = chat_scroll.scrollHeight;
            }
        }
        else {
            this.the_message=new ChatMessage();
            this.the_message.user = data['user'];
            this.the_message.message = data['message'];
            this.the_message.the_type = data['the_type'];
            this.the_message.timestamp = data['timestamp'];
            this.messages.push(this.the_message);
            const chat_scroll = document.getElementById('chat_div_space');
            chat_scroll.scrollTop = chat_scroll.scrollHeight;
         }
    };
   }

  ngOnInit() {
    this.mutationObserver = new MutationObserver((mutations) => {
        this.scrollToBottom();
        const chat_scroll = document.getElementById('chat_div_space');
        chat_scroll.scrollTop = chat_scroll.scrollHeight ;
      }
    );

    this.mutationObserver.observe(this.matList.nativeElement, {
        childList: true
    });
  }

  sendMessage(message,type:string) {
     if(this.dataService.profileImgIsSet()){
       if (message!==""){
         const now = new Date();
         const m = new ChatMessage();
         m.user=sessionStorage.getItem('username');
         m.message= message;
         m.the_type = type;
         m.timestamp= now.toLocaleString();
         this.websocket.send(
            JSON.stringify(m)
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
    // subscribing to any changes in the list of items / messages
  }

  // auto-scroll fix: inspired by this stack overflow post
  // https://stackoverflow.com/questions/35232731/angular2-scroll-to-bottom-chat-style
  private scrollToBottom(): void {
    try {
      this.matList.nativeElement.scrollTop = this.matList.nativeElement.scrollHeight;
    } catch (err) {}
  }






}
