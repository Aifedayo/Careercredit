import { Component, OnInit } from '@angular/core';
import * as $ from 'jquery'
import {ApiService} from "../../share/api.service";
import {environment} from "../../../environments/environment";
import {ClassModel} from "../../share/class-model";
import {Observable} from "rxjs/index";
import {UserModel} from "../../share/user-model";
import {DataService} from "../../data.service";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  public user$:Observable<UserModel>=null;
  public group$:Observable<ClassModel>=null;
  public environment = environment;

  constructor(
    private apiService:ApiService, 
    private dataservice: DataService,
  ) { }

  logout(){
    this.dataservice.logout(); 
  }

  public openClasses(){
    $('#sclass').click(function(){
      $('.dropdown-trigger').show()
    });
  }

  ngOnInit() {
    this.group$ = this.apiService.getGroupInfo(sessionStorage.getItem('active_group'))
    this.user$ = this.apiService.getUserInfo()
  }

  public getImgUrl(prevUrl){
    // return this.dataservice.profileImgIsSet()?
    //    environment.API_URL + (this.dataservice.updatedImgUrl || prevUrl):
    //    prevUrl;
    return this.dataservice.profileImgIsSet()?
       this.dataservice.updatedImgUrl || (environment.API_URL + prevUrl):
       prevUrl;
  }
}
