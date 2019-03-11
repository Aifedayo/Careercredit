import { Component, OnInit } from '@angular/core';
import {Observable} from "rxjs/index";
import {ApiService} from "../../share/api.service";
import {AttendanceModel} from "../../share/attendance-model";
import {ActivatedRoute, Router} from "@angular/router";
import {UserModel} from "../../share/user-model";

@Component({
  selector: 'app-attendance',
  templateUrl: './attendance.component.html',
  styleUrls: ['./attendance.component.css']
})
export class AttendanceComponent implements OnInit {

  public a;
  public attendance$;
  public user$:Observable<UserModel>;
  constructor(private apiService:ApiService,private router:ActivatedRoute) {

  }

  ngOnInit() {
    this.router.params.subscribe(data=>{

      this.attendance$=this.apiService.getUserAttendance(sessionStorage.getItem('active_group'),data['user_id'])
      this.user$=this.apiService.getUserInfo(data['user_id']);
    });
  }

}
