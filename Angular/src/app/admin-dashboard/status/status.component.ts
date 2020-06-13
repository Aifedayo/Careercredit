import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {UserModel} from "../../share/user-model";
import {environment} from "../../../environments/environment";
import {Observable} from "rxjs/index";
import {ApiService} from "../../share/api.service";

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.css']
})
export class StatusComponent implements OnInit {

  url = environment.API_URL;
  public a;
  public attendance$;
  public user$:Observable<UserModel>;
  constructor(private apiService:ApiService,private router:Router,private route:ActivatedRoute) {
  }

  ngOnInit() {
    console.log(this.route.params)
    this.route.params.subscribe(data=>{

      this.attendance$=this.apiService.getUserAttendance(sessionStorage.getItem('active_group'),data['user_id'])
      this.user$=this.apiService.getUserInfo(data['user_id']);
      console.log(window.location.origin)
    });
  }

  deleteUser(){
    var user: number;
    this.user$.subscribe(data => {
    user = data['id'];   
    console.log(user) 
    this.apiService.deleteUser(sessionStorage.getItem('active_group'), user).subscribe(
      data => {
        alert('Student has been removed')
        window.location.replace(window.location.origin+"/admin/students")
      }
    )
   })
  //  this.apiService.deleteUser(sessionStorage.getItem('active_group'), user)
  }

}
