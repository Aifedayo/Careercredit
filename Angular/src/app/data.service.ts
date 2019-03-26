import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import {ActivatedRoute,  Router} from '@angular/router';
import {environment} from "../environments/environment";
import {Location} from "@angular/common";
import {ApiService} from "./share/api.service";

@Injectable({
  providedIn: 'root'
})
export class DataService {

  public message;
  public login_username;
  public login_password;
  public createuser_email;
  public createuser_password;
  public createuser_username;
  public username;
  public id;
  public users;
    private headers: HttpHeaders = new HttpHeaders();


  public httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  };
  public authOptions;
  private required:boolean = false;
  private uploaded:boolean = true;


  constructor(private http: HttpClient, private router: Router,
              private route: ActivatedRoute,location:Location,
             ) {

  }


  static islogin() {
      return !!sessionStorage.getItem('token');
  }

  logout() {
    sessionStorage.clear()
    window.location.replace(environment.API_URL)
  }


   sessionSet(token:string,group_id:string)  {
    this.http.post(environment.API_URL + 'sso_api/confirm_key/' + group_id,JSON.stringify({'token':token}),this.httpOptions)
      .subscribe(data=>{
      sessionStorage.clear();
      sessionStorage.setItem('username', data['username']);
      sessionStorage.setItem('token', data['token']);
      sessionStorage.setItem('role', data['role']);
      sessionStorage.setItem('user_id', data['id']);
      sessionStorage.setItem('active_group', group_id);
      sessionStorage.setItem('video_required', data['video_required']);
      sessionStorage.setItem('uploaded', data['uploaded']);
      console.log(data['video_required'])
      console.log(data['uploaded'])
      if(!!data['video_required']){
        if(!data['uploaded']){
          console.log('video not uploaded')
          this.router.navigate(['/v'])
        }
        else {
               this.router.navigate(['/classroom', group_id])
        return true;
        }

      }
      else{
        console.log('video not required')
        this.router.navigate(['/classroom' ,group_id])
        return true;
      }



    },error => {
        alert('Cannot communicate with server, please try again')
      return false;
    })
  }
}

