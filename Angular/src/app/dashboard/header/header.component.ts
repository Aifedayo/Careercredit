import { Component, OnInit } from '@angular/core';
import * as $ from 'jquery'
import {ApiService} from "../../share/api.service";
import {ClassModel} from "../../share/class-model";
import {Observable} from "rxjs/index";
import {UserModel} from "../../share/user-model";

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  public user$:Observable<UserModel>=null;
  public group$:Observable<ClassModel>=null;
  constructor(private apiService:ApiService) { }

  public openClasses(){
    $('#sclass').click(function(){
      $('.dropdown-trigger').show()
    });


  }

  ngOnInit() {
    this.group$ = this.apiService.getGroupInfo(sessionStorage.getItem('active_group'))
    this.user$ = this.apiService.getUserInfo()

  }

}
