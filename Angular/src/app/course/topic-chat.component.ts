import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient } from '@angular/common/http';
import {environment} from "../../environments/environment.prod";
import {ApiService} from "../share/api.service";


@Component({
  selector: 'app-topic-chat',
  templateUrl: './topic-chat.component.html',
  styleUrls: ['./topic-chat.component.css']
})
export class TopicChatComponent implements OnInit {

  public users: Array<object> = [];
  public chat_text  = '';
  public messages = [];
  public websocket;
  public email;

  constructor(private http: HttpClient) {
    this.websocket = new WebSocket(environment.WS_URL);
    this.websocket.onopen = (evt) => {
      this.websocket.send(JSON.stringify({'user': sessionStorage.getItem('username'), 'message': '!join DjangoClass'}));
      };

      this.websocket.onmessage = (evt) => {
        const data = JSON.parse(evt.data);
        if (data['messages'] !== undefined) {
            this.messages = [];
            for (let i = 0; i < data['messages']['length']; i++) {
                this.messages.push(data['messages'][i]['user'] + ': ' + data['messages'][i]['message']);
            }
        } else {
            this.messages.push(data['user'] + ': ' + data['message']);
        }
        const chat_scroll = document.getElementById('chat_div_space');
        chat_scroll.scrollTop = chat_scroll.scrollHeight;
        console.log(this.messages);
    };
   }

  ngOnInit() {
    // this.dataservice.djangostudents().subscribe((data: Array<object>) => {
    //   this.users = data;
    // });
  }

  public allUsers() {
    // this.dataservice.djangostudents().subscribe((data: Array<object>) => {
    //   this.users = data;
    // });
  }

  sendMessage(message) {
    this.websocket.send(JSON.stringify({'user': sessionStorage.getItem('username'), 'message': this.chat_text}));
    this.chat_text = '';
  }
}
