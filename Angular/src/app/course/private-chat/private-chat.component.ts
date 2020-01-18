import { ActivatedRoute, Params, ParamMap } from '@angular/router';
import { Component, OnInit, ViewChild, ElementRef} from '@angular/core';
import { DataService } from '../../data.service';
import { HttpClient } from '@angular/common/http';
import { AlertService } from './../_alert/alert.service';
import { environment } from './../../../environments/environment';
import { Subscription } from 'rxjs';
import { WebSocketSubject, webSocket } from 'rxjs/webSocket';

export enum TYPE {Plain='plain', Image='image', File='file'}

@Component({
  selector: 'app-private-chat',
  templateUrl: './private-chat.component.html',
  styleUrls: ['./private-chat.component.css']
})

export class PrivateChatComponent implements OnInit {

  private users: Array<object> = [];
  public chat_text = '';
  public messages = [];
  public email;
  private user: {id: number, username: string};
  private activeGroup:string;
  private mutationObserver:MutationObserver;
  private routeParamSub: Subscription;
  public type=TYPE;
  private websocket$:WebSocketSubject<any>
  private token:string;

  @ViewChild('chatList', { read: ElementRef }) chatlist: ElementRef;

  constructor( 
    public dataservice: DataService, 
    private http: HttpClient, 
    private route: ActivatedRoute,
    private alertService:AlertService
  ) {
    this.token = sessionStorage.getItem('token');
    this.dataservice.username = sessionStorage.getItem('username');
    this.websocket$ = webSocket(environment.WS_URL+"?token="+this.token);
   }

  ngOnInit() {
    this.callWebsocket();
    this.routeParamSub = this.route.params.subscribe(params => {
      this.changePartner(+params['id']);
    });
  }

  ngAfterViewInit(){
    this.mutableObserver();
  }

  ngOnDestroy(): void {
    this.routeParamSub.unsubscribe()
  }

  changePartner(partner){
    this.messages = [];
    const partner_id = partner;
    const prepare_group = [
      partner_id,
      sessionStorage.getItem('user_id')
    ];
    this.activeGroup = prepare_group.sort().join('_');
    
    this.websocket$.next({
      action:'getRecentMessages',
      active_group:this.activeGroup,
      token:this.token
    });
  }

  sendMessage(message, type:string) {
    if(this.dataservice.profileImgIsSet()){
      if(message!==''){
        const now = new Date();
        this.websocket$.next({
            action:'sendMessage',
            active_group:this.activeGroup,
            user: this.dataservice.username, 
            content: message,
            the_type:type,
            timestamp:now.toLocaleDateString(),
            token:this.token
        });
      }
      
      this.chat_text = '';
    }
    else
    {
      this.alertService.error(
        'You need to set your profile image to continue'
      );
    }
  }

  callWebsocket(){
    this.websocket$.subscribe((messages)=>{
      if(messages['active_group'] == this.activeGroup){
        if (messages['messages'] !== undefined) {
          messages['messages'].forEach((message)=>{
              const messg = message.user+': '+message.content;
              this.messages.push(messg);
            }
          );
        }
      }
    });
  }

  mutableObserver(){
    this.mutationObserver = new MutationObserver((mutations) => {
        this.scrollToBottom();
      }
    );

    this.mutationObserver.observe(this.chatlist.nativeElement, {
        childList: true
    });
  }

  private scrollToBottom(){
    try {
      this.chatlist.nativeElement.scrollTop = 
      this.chatlist.nativeElement.scrollHeight;
      const chat_scroll = document.getElementById('chat_div_space');
      chat_scroll.scrollTop = chat_scroll.scrollHeight;
    } catch (err) {}
  }

}
