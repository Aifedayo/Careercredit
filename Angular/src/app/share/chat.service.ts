import { Injectable } from '@angular/core';
import {Subject} from "rxjs/index";
import {WebSocketService} from "./web-socket.service";
import {environment} from "../../environments/environment";
declare var moment: any;

@Injectable({
  providedIn: 'root'
})



export class ChatService {

  public messages: Subject<Message>;

	// constructor(wsService: WebSocketService) {
	// 	this.messages = <Subject<Message>>wsService
	// 		.connect(environment.WS_URL)
    //
	// 	 .map((response: MessageEvent): Message => {
	// 			let data = JSON.parse(response.data);
	// 			return {
	// 				author: data.author,
	// 				message: data.message
	// 			}
	// 		});
	// }
	public formatProfileImg(proImgUrl:string){
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

  public formatTime(timestamp){
    return timestamp.indexOf(':')== -1?
    moment(Number(timestamp)).format('LT'):timestamp
  }

}

export interface Message {
	author: string,
	message: string
}
