import { Component, OnInit } from '@angular/core';
import {ApiService} from "../../share/api.service";
import {Observable} from "rxjs/index";
import {ClassModel} from "../../share/class-model";
import {environment} from "../../../environments/environment";

import {DataService} from "../../data.service";

@Component({
  selector: 'app-course-list',
  templateUrl: './course-list.component.html',
  styleUrls: ['./course-list.component.css']
})
export class CourseListComponent implements OnInit {

  public courses$:Observable<ClassModel[]>;
  public username:any;
  public environment = environment;

  constructor(private apiService:ApiService,private dataservice: DataService) {
    this.username=sessionStorage.getItem('username');
  }

  ngOnInit() {
    this.courses$=this.apiService.getAvailableClasses();
  }

  addcourse(){
    this.dataservice.addcourse();
  }

  getProfileImg(proImgUrl:string){
    var image_url = "";
      if(proImgUrl === null){
        return null;
      }
      
      if(
        proImgUrl.startsWith("https://") || 
        proImgUrl.startsWith("http://") 
      ){
        image_url =  proImgUrl
      }
      else {
        image_url = environment.API_URL + proImgUrl
      }
    return image_url
  }

}
