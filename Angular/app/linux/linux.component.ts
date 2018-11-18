import { Component, OnInit } from '@angular/core';
import { DataService } from '../data.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MaterializeModule} from 'angular2-materialize';

@Component({
  selector: 'app-linux',
  templateUrl: './linux.component.html',
  styleUrls: ['./linux.component.css'],
  providers: [MaterializeModule]
})
export class LinuxComponent implements OnInit {

   users: any = [];
   options = {};

  constructor(public dataservice: DataService, private http: HttpClient, public materializedirective: MaterializeModule ) {


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
    this.dataservice.djangostudents().subscribe((data) => {
      this.users = data;
    });
  }

  logout() {
    this.dataservice.logout();
  }

}
