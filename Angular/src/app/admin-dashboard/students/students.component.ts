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
  public user = new UserModel();
  public attendances
  constructor( private apiService:ApiService) {
    this.students=apiService.getMembers(sessionStorage.getItem('active_group'))
  }

  ngOnInit() {
    this.students.subscribe(
      student =>{
        student.map(a =>{
          // console.log(a['id'])
          this.apiService.getUserAttendance(sessionStorage.getItem('active_group'), a.id).subscribe(attendance=>{
                  console.log(typeof(attendance))
                  attendance
                }
              )          
            }
          )
      }
    )
    
  }
  

  deleteByDate(data:Date){
    this.students.subscribe(
      student =>{
        console.log(student)

      }
    )
  }
}
