import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import * as $ from 'jquery';
// import { MaterializeModule } from 'angular2-materialize';

@Component({
  selector: 'app-course2',
  templateUrl: './course2.component.html',
  styleUrls: ['./course2.component.css']
})
export class Course2Component implements OnInit {

  public users: Array<object> = [];
  public options = {};

  constructor(public dataservice: DataService, private http: HttpClient) {


    this.dataservice.username = sessionStorage.getItem('username');

    this.dataservice.authOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json', 'Authorization': 'JWT ' + sessionStorage.getItem('token')})
    };

  }

  ngOnInit() {
    // this.dataservice.groupclassusers().subscribe((data: Array<object>) => {
    //   this.users = data;
    //   console.log(data);

    // });
  }

  logout() {
    this.dataservice.logout();
  }

}
