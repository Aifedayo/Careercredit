import { Component, OnInit, Input, Output, EventEmitter  } from '@angular/core';
import { environment } from './../../../environments/environment';
import { ChatService } from './../../share/chat.service';

@Component({
  selector: 'app-others-chat',
  templateUrl: './others-chat.component.html',
  styleUrls: ['./others-chat.component.css'],
})
export class OthersChatComponent implements OnInit {
    public current_user:string;

    @Output() qouted = new EventEmitter();
    @Input() message = {};
    
    constructor(public chatService:ChatService){
        this.current_user = sessionStorage.getItem('username');
    }

    ngOnInit(): void {

    }   

    isOthers(username){
        return username !== this.current_user && 
        username !== 'DATE-INFO'
    }

    qoute(){
        this.qouted.emit(this.message)
    }
}