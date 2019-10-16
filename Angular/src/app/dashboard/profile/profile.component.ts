import { Component, OnInit } from '@angular/core';
import {environment} from "../../../environments/environment";
import {ApiService} from "../../share/api.service";
import {UserModel} from "../../share/user-model";
import * as $ from 'jquery';
import { DataService } from 'src/app/data.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  public user = new UserModel();
  public attendance$;
  public environment = environment;

  constructor(private apiService:ApiService, private dataService:DataService) {} 

  ngOnInit() {
    this.apiService.getUserInfo(
      sessionStorage.getItem('user_id')
    ).subscribe(data=>{
      this.user.username=data['username'];
      this.user.first_name=data['first_name']
      this.user.last_name=data['last_name']
      // this.user.profile_img= data['profile_img']
      this.user.profile_img= this.getProfileImg(data['profile_img'])
      this.user.id=data['id']
    });
    this.attendance$=this.apiService.getUserAttendance(
      sessionStorage.getItem('active_group')
    )
  }

  fileChange(event): void {
      const fileList: FileList = event.target.files;
      if (fileList.length > 0) {
          const file = fileList[0];

          const formData = new FormData();
          formData.append('file', file, file.name);

          this.apiService.uploadImage(formData)
            .subscribe(
                data => {
                  sessionStorage.setItem('profile_img', data['profile_img'])
                  this.user.profile_img=this.getProfileImg(
                    data['profile_img']
                  )
                  this.dataService.updatedImgUrl = this.getProfileImg(
                    data['profile_img']
                  )
                },
                error => console.log( error)
            );
      }
  }

  updateInfo(event): void {
    this.apiService.updateUserInfo(this.user).subscribe(data=>{
      this.user.username=data['username'];
      this.user.first_name=data['first_name']
      this.user.last_name=data['last_name']
      // this.user.profile_img=data['profile_img']
      this.user.id=data['id']
      }
    );
  }

  getProfileImg(proImgUrl:string){
    return this.dataService.profileImgIsSet()?
        environment.API_URL + proImgUrl:proImgUrl;
  }
}
