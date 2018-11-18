import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-topic-chat',
  templateUrl: './topic-chat.component.html',
  styleUrls: ['./topic-chat.component.css']
})
export class TopicChatComponent implements OnInit {


  public URL = '54.244.162.68:8001';
  public users: Array<object> = [];
  public chat_text  = '';
  public messages = [];
  public websocket;
  public email;

  constructor(public dataservice: DataService, private http: HttpClient) {
    this.dataservice.username = sessionStorage.getItem('username');
    this.websocket = new WebSocket('ws://' + '54.244.162.68:8001');
    this.websocket.onopen = (evt) => {
      this.websocket.send(JSON.stringify({'user': this.dataservice.username, 'message': '!join DjangoClass'}));
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
    this.dataservice.djangostudents().subscribe((data: Array<object>) => {
      this.users = data;
    });
  }

  public allUsers() {
    this.dataservice.djangostudents().subscribe((data: Array<object>) => {
      this.users = data;
    });
  }

  sendMessage(message) {
    this.websocket.send(JSON.stringify({'user': this.dataservice.username, 'message': this.chat_text}));
    this.chat_text = '';
  }
}
