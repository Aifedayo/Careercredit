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
    // let dt = new Date('Tuesday 17 December, 2019')
    // let pdt = new Date('2020-06-10')
    // console.log(date.valueAsDate)
    // console.log(dt)
    // 
    this.students.subscribe(
      student =>{
        
        student.map(a =>{
          let user_id =a['id']
          this.attendance = this.apiService.getUserAttendance(sessionStorage.getItem('active_group'), user_id)
          
          this.attendance.subscribe(b=>{
            const last_login = b[0]
            if(last_login){
                // console.log(last_login)
                // console.log(c)  
              const last_login_date = new Date( last_login.timestamp.slice(0, -10))
              // console.log(last_login_date)
              // console.log(date.valueAsDate)
              if (date.valueAsDate >= last_login_date){
                // console.log('hi')
                this.apiService.deleteUser(sessionStorage.getItem('active_group'), user_id).subscribe(
                  data => {
                    console.log()
                  }
                )
              } 
            }

          })
              
            }
          )
          setTimeout(()=>{
            alert('Students has been removed')
            window.location.replace(window.location.origin+"/admin/students")
          }, 2000)

      }
    )

  }
}
