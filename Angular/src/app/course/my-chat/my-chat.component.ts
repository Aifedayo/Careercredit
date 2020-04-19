import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ChatService } from './../../share/chat.service';
import { UserModel } from './../../share/user-model';
import { Observable } from 'rxjs';
import { ApiService } from './../../share/api.service';

@Component({
  selector: 'app-my-chat',
  templateUrl: './my-chat.component.html',
  styleUrls: ['./my-chat.component.css'],
})
export class MyChatComponent implements OnInit {
    public current_user:string;
    private user$: Observable<UserModel>;

    @Input() message = {};
    @Output() qouted = new EventEmitter();

    constructor(public chatService:ChatService,private apiService:ApiService){
        this.user$ = this.apiService.getUserInfo();
        this.current_user = sessionStorage.getItem('username');
    }

    ngOnInit(): void {
    }

    qoute(){
      this.qouted.emit(this.message)
    }
}