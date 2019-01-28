import {Component, ElementRef, OnInit, QueryList, ViewChild, ViewChildren} from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient } from '@angular/common/http';
import {environment} from "../../environments/environment.prod";
import {ApiService} from "../share/api.service";
import {ChatMessage} from "../share/chat-message";
import {Observable} from "rxjs/index";
import {MatList, MatListItem} from "@angular/material";

export enum TYPE {Plain='plain', Image='image', File='file'}

@Component({
  selector: 'app-topic-chat',
  templateUrl: './topic-chat.component2.html',
  styleUrls: ['./topic-chat.component.css']
})




export class TopicChatComponent implements OnInit {



  public users: Array<object> = [];
  public chat_text  = '';
  public messages = [];
  public the_message:ChatMessage;
  public websocket;
  public email;
  public type=TYPE;
  constructor(private http: HttpClient, private apiService:ApiService) {
    this.websocket = new WebSocket(environment.WS_URL);
    this.websocket.onopen = (evt) => {
      const now=new Date();
      const m= new ChatMessage()
      m.user=sessionStorage.getItem('username')
      m.type = 'plain';
      m.message="!join Djangoclass"
      m.timestamp= now.toString();
      this.websocket.send(JSON.stringify(m));
      };

      this.websocket.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        if (data['messages'] !== undefined) {
            for (let i = 0; i < data['messages']['length']; i++) {
              this.the_message=new ChatMessage()
              this.the_message.user = data['messages'][i]['user'];
              this.the_message.message = data['messages'][i]['message'];
              this.the_message.timestamp = data['messages'][i]['timestamp'];
              this.the_message.type = data['messages'][i]['type'];
              this.messages.push(this.the_message);
                   const chat_scroll = document.getElementById('chat_div_space');
        chat_scroll.scrollTop = chat_scroll.scrollHeight;
                // // this.messages.push(data['messages'][i]['user'] + ': ' + data['messages'][i]['message']);
                // this.messages.push(data['messages'][i]['user'] + ': ' + data['messages'][i]['message']);
            }
        }
        else {
            this.the_message=new ChatMessage()
            this.the_message.user = data['user'];
            this.the_message.message = data['message'];
            this.the_message.type = data['type'];
            this.the_message.timestamp = data['timestamp'];
            // this.messages.push(data['user'] + ': ' + data['message']);
            this.messages.push(this.the_message);
        }
        const chat_scroll = document.getElementById('chat_div_space');
        chat_scroll.scrollTop = chat_scroll.scrollHeight;
    };
   }

  ngOnInit() {
    // this.dataservice.djangostudents().subscribe((data: Array<object>) => {
    //   this.users = data;
    // });

  }

   sendMessage(message,type:string) {
    let now = new Date();
    let m = new ChatMessage();
    m.user=sessionStorage.getItem('username');
    m.message= message;
    m.type = type;
    m.timestamp= now.toString()
    this.websocket.send(
      JSON.stringify(m)
    );
    this.chat_text = '';
  }
  openImage(url):void{


  }
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
    this.matListItems.changes.subscribe(elements => {
      this.scrollToBottom();
    });
  }

  // auto-scroll fix: inspired by this stack overflow post
  // https://stackoverflow.com/questions/35232731/angular2-scroll-to-bottom-chat-style
  private scrollToBottom(): void {
    try {
      this.matList.nativeElement.scrollTop = this.matList.nativeElement.scrollHeight;
    } catch (err) {
    }
  }


    // getting a reference to the overall list, which is the parent container of the list items
  @ViewChild(MatList, { read: ElementRef }) matList: ElementRef;

  // getting a reference to the items/messages within the list
  @ViewChildren(MatListItem, { read: ElementRef }) matListItems: QueryList<MatListItem>;



}
