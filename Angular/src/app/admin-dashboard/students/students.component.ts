import { Component, OnInit } from '@angular/core';
import {ApiService} from "../../share/api.service";
import {UserModel} from "../../share/user-model";
import {Observable} from "rxjs/index";
import { stringify } from 'querystring';

@Component({
  selector: 'app-students',
  templateUrl: './students.component.html',
  styleUrls: ['./students.component.css']
})
export class StudentsComponent implements OnInit {

  public students:Observable<UserModel[]>;
  public user = new UserModel();
  public attendances
  public attendance
  constructor( private apiService:ApiService) {
    this.students=apiService.getMembers(sessionStorage.getItem('active_group'))
  }

  ngOnInit() {

    
  }
  

  deleteByDate(date: HTMLInputElement){
    this.students.subscribe(
      student =>{
        student.map(a =>{
          let user_id =a['id']
          this.attendance = this.apiService.getUserAttendance(sessionStorage.getItem('active_group'), user_id)
            
          this.attendance.subscribe(b=>{
            b.map(c =>{
              let last_login = c.timestamp.slice(0, -10)
              console.log(last_login)
              
              if (last_login == date.value){
                console.log('hi')
                this.apiService.deleteUser(sessionStorage.getItem('active_group'), user_id).subscribe(
                  data => {
                    alert('Students has been removed')
                    window.location.replace(window.location.origin+"/admin/students")
                  }
                )
              }
            })
          })
              
            }
          )
      }
    )
  }
}
