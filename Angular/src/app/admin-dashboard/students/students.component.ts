import { Component, OnInit } from '@angular/core';
import {ApiService} from "../../share/api.service";
import {UserModel} from "../../share/user-model";
import {Observable, forkJoin} from "rxjs/index";
import { stringify } from 'querystring';
import {map, tap} from "rxjs/operators"
import { last } from '@angular/router/src/utils/collection';

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
  public last_login_arr: Observable<any>[] = []
  constructor( private apiService:ApiService) {
    this.students=apiService.getMembers(sessionStorage.getItem('active_group'))
  }

  ngOnInit() {

    
  }
  
  deleteByDate(date: HTMLInputElement){
    let students_id = this.getStudentsId()
    students_id.subscribe(res=>{
      res.forEach(val1=>{
        this.attendance = this.apiService.getUserAttendance(sessionStorage.getItem('active_group'), val1)
        const last_login = this.attendance.pipe(
          map(att =>{ return  [val1, att[0]] })
        )
        this.last_login_arr.push(last_login)  
      })
      
      forkJoin(this.last_login_arr).subscribe((arr)=>{
          arr.forEach(val2=>{
            // console.log(val2)
            if(val2[1]){
              const last_login_date = new Date( val2[1].timestamp.slice(0, -10))
              // console.log(val2)
              if (date.valueAsDate >= last_login_date){
                console.log('wil be deleted')
                this.apiService.deleteUser(sessionStorage.getItem('active_group'), val2[0]).subscribe()
              }
            }
          })
        },
        (error)=>{},
        ()=>{
          alert('Students have been removed')
          window.location.replace(window.location.origin+"/admin/students")
        }
      )
      // console.log(this.last_login_arr)
      
    },
    (error)=>{

    },
    ()=>{
      // console.log("hi")
    }
    )
    
  }
  getStudentsId(){
    return this.students.pipe(map(val=>{return val.map(val1=>{return val1.id})}))
  }
  // deleteByDate(date: HTMLInputElement){
  //   let delete_stds = this.students.pipe(
  //     tap(val=>{
  //     val.map(a=> {
  //       let user_id =a['id']
  //       this.attendance = this.apiService.getUserAttendance(sessionStorage.getItem('active_group'), user_id).
  //       pipe(tap(b=>{
  //         const last_login = b[0]
  //         if(last_login){
  //           console.log(last_login)
  //           const last_login_date = new Date( last_login.timestamp.slice(0, -10))
  //             if (date.valueAsDate >= last_login_date){
  //               this.apiService.deleteUser(sessionStorage.getItem('active_group'), user_id).subscribe(
  //                 data => {
  //                   console.log()
  //                 }
  //               )
  //             }
  //         }
  //         return(last_login)
  //       }))
  //       this.attendance.subscribe(res=>{
  //         console.log()
  //       })
        
  //     })

  //   })
  //   )
  //   delete_stds.subscribe(
      //  ()=> {},
      //  ()=> {},
      //  ()=> {
      //   setTimeout(()=>{
      //             alert('Students has been removed')
      //             window.location.replace(window.location.origin+"/admin/students")
      //           }, 2000)
      //  },
  // )







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

  // }
}
