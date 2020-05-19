import { Component, OnInit } from '@angular/core';
import {ApiService} from "../../share/api.service";
import {UserModel} from "../../share/user-model";
import {Observable} from "rxjs/index";

@Component({
  selector: 'app-students',
  templateUrl: './students.component.html',
  styleUrls: ['./students.component.css']
})
export class StudentsComponent implements OnInit {

  public students:Observable<UserModel[]>;
  constructor( private apiService:ApiService) {
    this.students=apiService.getMembers(sessionStorage.getItem('active_group'))
  }

  ngOnInit() {

  }

}
