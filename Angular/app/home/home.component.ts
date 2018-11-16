import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  private users: Array<object> = [];
  public chat_text = '';
  public messages = [];
  public websocket;
  public email;

  constructor(public dataservice: DataService, private http: HttpClient) {}

  ngOnInit() {
   }

  login() {
    this.dataservice.login();
  }

}
