import {Component, ElementRef, OnInit,  ViewChild} from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient } from '@angular/common/http';

import {ApiService} from "../share/api.service";
import {ChatMessage} from "../share/chat-message";
import {Observable, Subject, BehaviorSubject} from "rxjs/index";
import { debounceTime, distinctUntilChanged, switchMap, tap, scan, map, filter} from 'rxjs/operators';
import {MatList} from "@angular/material";
import {environment} from "../../environments/environment";
import {UserModel} from "../share/user-model";
import { AlertService } from './_alert/alert.service';
import ReconnectingWebSocket from '../_websocket/reconnecting-websocket';
import { FormControl, FormGroup, Validators } from '@angular/forms';


declare var moment: any;

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
  public websocket: ReconnectingWebSocket;
  public ws: WebSocket;
  public email;
  public type=TYPE;
  public avatar:string;
  private token:string;
  public offset_id:Number = 0;
  private is_send_message:Boolean = false;
  private recent_message_is_set:Boolean = false;
  public mention_users: Observable<any[]>;
  private search_mention_stream = new Subject();
  public qoute_message = null;
  public mentionConfig;


  // getting a reference to the overall list, which is the parent container of the list items
  @ViewChild(MatList, { read: ElementRef }) matList: ElementRef;
  @ViewChild('ChatSpace') chatSpace: ElementRef<HTMLElement>;
  @ViewChild('chat_input') chat_input: ElementRef<HTMLElement>;

  private user$: Observable<UserModel>;
  public environment = environment;

  //is-typing 
  public messageForm = new FormGroup({
    message: new FormControl('', Validators.required)
    });
  public messageInput = new Subject<string>();
  public touched: Subject<boolean> = new BehaviorSubject(false);
  public typingIndicator : Observable<boolean>//
  private _whoIsTypingArr: string[] = [];
  private whoIsTyping$: Subject<string[]> = new BehaviorSubject([]);
  public who: Observable<string>
  public test

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
      this.websocket = new ReconnectingWebSocket(
        environment.WS_URL+"?token="+this.token
      )
      this.ws = new WebSocket(environment.WS_URL+"?token="+this.token)
      this.mentionConfig = {
        dropUp:'true',
        allowSpace:'true',
        mentionSelect: (item:any)=>{
          // return `<b>${item['label'].toUpperCase()}</b>`;
          return `@${item['label']} `;
        }
      };
   }

  ngOnInit() {
    this.callWebsocket()
    this.setUserMentionProp()
  }

  ngAfterViewInit(): void {
    this.mutableObserver();
    this.messageForm.valueChanges.pipe(
      tap(() => 
      this.startTyping()),
      ).subscribe();
    this.messageInput.pipe(
      tap(() => this.startTyping()),
      ).subscribe();
    
    this.who = this.getTypingIndicator().pipe(filter(val => val.length > 0), map(val => {
      switch(val.length) {
      case 1: return `${val[0]} is typing`;
      case 2: return `${val[0]} and ${val[1]} are typing`;
      default: return `Many people are typing`;
      }
      }));
  }

  setUserMentionProp(){
    this.mention_users = this.search_mention_stream.pipe(
      debounceTime(250),
      distinctUntilChanged(),
      switchMap((data: any) => this.apiService.getMentionUsers(data))
    )
    // .debounceTime(500)
    // .distinctUntilChanged()
    // // .switchMap((term: string) => this.getItems(term));
  }

  sendMessage(message,type:string) {
     if(this.dataService.profileImgIsSet()){
       if(message!==""){
          const now = new Date();
          let context = {
            action:'sendMessage',
            active_group:this.activeGroup,
            user:sessionStorage.getItem('username'),
            content:message,
            the_type:type,
            timestamp:now.getTime(),
            // timestamp:this.onlyHsMs(now.toLocaleTimeString()),
            token:this.token
          }; 

          if(this.qoute_message){
            let {profile_img, ...qoute_m} = this.qoute_message
            context['qoute_message'] = qoute_m
          }
          console.log('sent')
          this.websocket.send(JSON.stringify(context));
          this.qoute_message = null;
          this.chat_text = '';
          this.is_send_message = true
          
        } 
      }
      else{
          this.alertService.error(
            'You need to set your profile image to continue'
          );
      }
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
                  // const url=environment.API_URL + data['url'];
                  this.sendMessage(data['url'],data['type'])
                },
                error => console.log( error)
            );
      }
  }

  callWebsocket(){
    // this.websocket = new WebSocket(
    //   environment.WS_URL+"?token="+this.token
    // );

    this.websocket.onopen = (evt) => {
      
      if(!this.recent_message_is_set){
        this.getMessages()
      }
    };

    this.websocket.onmessage = (evt) => {
      const data = JSON.parse(evt.data);
      // console.log(data)
      this.processMessages(data)
    };

    // this.websocket.onclose = ()=>{
    //     // this.websocket = null
    //     console.log('... trying reconnection in 5 sec....')
    //     setTimeout(this.callWebsocket,5000)
    // }
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

  searchMention(search_txt: string) {
    const data = {
      active_group:this.activeGroup,
      search_text:search_txt,
      token:this.token
    };  
    this.search_mention_stream.next(data);
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

  qoute(message){
    this.qoute_message = message
    this.chat_input.nativeElement.focus()
  }

  closed(){
    this.qoute_message = null
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
    // console.log('hi')
    if(data['active_group'] == this.activeGroup){
      if(data['message'] === 'start_typing'){
        this.onTypingStarted(data["who"])
        this.typingIndicator = this.getTypingIndicator().pipe(map(val => val.length > 0));
      }
      else if(data['message'] === 'end_typing'){
        console.log("typing ended")
        this.onTypingEnded(data["who"])
      }
      if (data['messages'] !== undefined) {    
        if(data['is_next']){
          this.messages = [...data['messages'],...this.messages]
          this.chatSpace.nativeElement.scrollTop = 100
        }
        else if(data['from_where'] === 'send'){
          this.messages = [...this.messages,...data['messages']]
          this.is_send_message = true
        }
        else{
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
  public onTypingStarted (who) {
    console.log(this._whoIsTypingArr)
    if(this._whoIsTypingArr.indexOf(who) == -1){
      console.log('added')
    this._whoIsTypingArr.push(who);
    this.whoIsTyping$.next(this._whoIsTypingArr);
    }
  }

  public onTypingEnded (who) {
    this._whoIsTypingArr.splice(this._whoIsTypingArr.findIndex(val => val === who), 1);
    this.whoIsTyping$.next(this._whoIsTypingArr);
    }

  public getTypingIndicator(): Observable<any> {
    return this.whoIsTyping$;
    }

  public startTyping(): void {
    
    let context = {
      action:'startTyping',
      active_group:this.activeGroup,
      user:sessionStorage.getItem('username'),
      token:this.token
    }; 
    this.websocket.send(JSON.stringify(context));
    // CometChat.startTyping(new CometChat.TypingIndicator('supergroup', CometChat.RECEIVER_TYPE.GROUP, {}));
    }

  public endTyping(): void {
    console.log('hi')
    let context = {
      action:'endTyping',
      active_group:this.activeGroup,
      user:sessionStorage.getItem('username'),
      token:this.token
    }; 
    this.websocket.send(JSON.stringify(context));
  // CometChat.endTyping(new CometChat.TypingIndicator('supergroup', CometChat.RECEIVER_TYPE.GROUP, {}));
  }
  public isTyping(event){
    this.messageInput.next(event)
    // console.log("is typing")
    return true
  }

}
