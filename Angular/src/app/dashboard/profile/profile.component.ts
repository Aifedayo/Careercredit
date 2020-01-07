import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import {environment} from "../../../environments/environment";
import {ApiService} from "../../share/api.service";
import {UserModel} from "../../share/user-model";
// import * as $ from 'jquery';
import { DataService } from 'src/app/data.service';
import processHelper from './process.helper'
import { AlertService } from './../../course/_alert/alert.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {

  public user = new UserModel();
  public attendance$;
  public environment = environment;
  private fileName='';
  public isUploading:boolean=false

  constructor(
    private apiService:ApiService, 
    private dataService:DataService,
    private alertService: AlertService
  ) {} 

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
          this.isUploading = true
          this.user.profile_img=processHelper.loadingImage
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
                  this.isUploading = false
                },
                error => console.log( error)
            );
      }
  }

  changeImage(e):void{
    const file = e.dataTransfer ? 
      e.dataTransfer.files[0] : e.target.files[0];
    const pattern = /image-*/;
    const reader = new FileReader();
    if (!file.type.match(pattern)) {
      alert('invalid format');
      return;
    }
    this.fileName = file.name;
    reader.onload = this._handleReaderLoaded.bind(this);
    reader.readAsDataURL(file);
  }

  updateInfo(event): void {
    this.apiService.updateUserInfo(this.user).subscribe(data=>{
        this.user.username=data['username'];
        this.user.first_name=data['first_name']
        this.user.last_name=data['last_name']
        // this.user.profile_img=data['profile_img']
        this.user.id=data['id']
        this.alertService.success(
          'Profile successfully updated'
        );
      }
    );
  }

  getProfileImg(proImgUrl:string){
    var image_url = "";
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

  

  _handleReaderLoaded(e) {
    let reader = e.target;
    const body = {
      name:this.fileName,
      file:reader.result
    };
    // console.log(body);
    // this.apiService.uploadBase64Image(body)
    //   .subscribe(
    //       data => {
    //         const new_img_url = data['profile_img']+"?r="+Math.random()
    //         sessionStorage.setItem('profile_img', new_img_url);
    //         this.user.profile_img=this.getProfileImg(new_img_url);
    //         this.dataService.updatedImgUrl = this.getProfileImg(
    //           new_img_url
    //         )
    //       },
    //       error => console.log( error)
    //   );
    // console.log(reader.result)
  }
}
