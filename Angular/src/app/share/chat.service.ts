import { Injectable } from '@angular/core';
import {Subject} from "rxjs/index";
import {WebSocketService} from "./web-socket.service";
import {environment} from "../../environments/environment.prod";

@Injectable({
  providedIn: 'root'
})



export class ChatService {

  public messages: Subject<Message>;

	constructor(wsService: WebSocketService) {
		this.messages = <Subject<Message>>wsService
			.connect(environment.WS_URL)

			.map((response: MessageEvent): Message => {
				let data = JSON.parse(response.data);
				return {
					author: data.author,
					message: data.message
				}
			});
	}
}

export interface Message {
	author: string,
	message: string
}
