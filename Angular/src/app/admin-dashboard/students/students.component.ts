import { Component, OnInit } from '@angular/core';
import {ApiService} from "../../share/api.service";
import {UserModel} from "../../share/user-model";
import {Observable} from "rxjs/index";
import { stringify } from 'querystring';
import {map, tap} from "rxjs/operators"

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
    let delete_stds = this.students.pipe(
      tap(val=>{
      val.map(a=> {
        let user_id =a['id']
        this.attendance = this.apiService.getUserAttendance(sessionStorage.getItem('active_group'), user_id).
        pipe(tap(b=>{
          const last_login = b[0]
          if(last_login){
            console.log(last_login)
            const last_login_date = new Date( last_login.timestamp.slice(0, -10))
              if (date.valueAsDate >= last_login_date){
                this.apiService.deleteUser(sessionStorage.getItem('active_group'), user_id).subscribe(
                  data => {
                    console.log()
                  }
                )
              }
          }
          return(last_login)
        }))
        this.attendance.subscribe(res=>{
          console.log()
        })
        
      })

    })
    )
    delete_stds.subscribe(
       ()=> {},
       ()=> {},
       ()=> {
        setTimeout(()=>{
                  alert('Students has been removed')
                  window.location.replace(window.location.origin+"/admin/students")
                }, 2000)
       },
  )
  //NEW IMPLEMENTATION ABOVE
    // this.students.subscribe(res=>{
    //   console.log(res)
    // })
    // this.students.subscribe(
    //   student =>{
    //     student.map(a =>{
    //       let user_id =a['id']
    //       this.attendance = this.apiService.getUserAttendance(sessionStorage.getItem('active_group'), user_id)
          
    //       this.attendance.subscribe(b=>{
    //         const last_login = b[0]
    //         if(last_login){
    
    //           const last_login_date = new Date( last_login.timestamp.slice(0, -10))
         
    //           if (date.valueAsDate >= last_login_date){
    //             this.apiService.deleteUser(sessionStorage.getItem('active_group'), user_id).subscribe(
    //               data => {
    //                 console.log()
    //               }
    //             )
    //           } 
    //         }

    //       })
              
    //         }
    //       )
    //   },
    //   ()=>{},
    //   ()=> {
    //     setTimeout(()=>{
    //       alert('Students has been removed')
    //       window.location.replace(window.location.origin+"/admin/students")
    //     }, 2000)
    //   }
    // )

  }
}
