import { Component, OnInit } from '@angular/core';
import { DataService } from '../../data.service';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-private-chat',
  templateUrl: './private-chat.component.html',
  styleUrls: ['./private-chat.component.css']
})

export class PrivateChatComponent implements OnInit {

  public URL = '54.244.162.68:8001';

  private users: Array<object> = [];
  public chat_text = '';
  public messages = [];
  public websocket;
  public email;

  constructor( public dataservice: DataService, private http: HttpClient) {
    this.dataservice.username = sessionStorage.getItem('username');
    this.websocket = new WebSocket('ws://' + '54.244.162.68:8001');
    this.websocket.onopen = (evt) => {
      this.websocket.send(JSON.stringify({'user': this.dataservice.username, 'message': '!join room' + this.dataservice.id}));
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
  }




  sendMessage(message) {
    this.websocket.send(JSON.stringify({'user': this.dataservice.username, 'message': this.chat_text}));
    this.chat_text = '';
  }

}
