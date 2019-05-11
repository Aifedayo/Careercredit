
import { Component, OnInit } from '@angular/core';
import {ApiService} from "../../share/api.service";
import {Observable} from "rxjs/index";
import {ClassModel} from "../../share/class-model";
import {DataService} from "../../data.service";

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {

  public courses$:Observable<ClassModel[]>;
  public username:any;
  constructor(private apiService:ApiService,private dataservice: DataService) {
    this.username=sessionStorage.getItem('username');
  }


  ngOnInit() {
      this.courses$=this.apiService.getAvailableClasses();
  
  }
  addcourse(){
    this.dataservice.addcourse();
  }

}
