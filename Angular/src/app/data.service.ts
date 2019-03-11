import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import {ActivatedRoute,  Router} from '@angular/router';
import {environment} from "../environments/environment";
import {Location} from "@angular/common";

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

  public httpOptions = {
    headers: new HttpHeaders({'Content-Type': 'application/json'})
  };
  public authOptions;

  constructor(private http: HttpClient, private router: Router,private route: ActivatedRoute,location:Location) { }

  djangostudents() {
    return this.http.get( environment.API_URL + '');
  }

  createUser() {
    this.http.post( environment.API_URL + 'sso_api/login', JSON.stringify({'email': this.createuser_email, 'password': this.createuser_password, 'username': this.createuser_username}), this.httpOptions).subscribe(
        data => {
            this.message = data['message'];
            this.createuser_email = '';
            this.createuser_password = '';
            this.createuser_username = '';
            this.id = '';
        },
        err => {
            this.message = 'User Creation Failed! Unexpected Error!';
            console.error(err);
            this.createuser_email = '';
            this.createuser_password = '';
            this.createuser_username = '';
        }
    );
  }

  login() {
    this.http.post( environment.API_URL + 'sso_api/login', JSON.stringify({'username': this.login_username, 'password': this.login_password}), this.httpOptions).subscribe(
        data => {

            sessionStorage.setItem('username', data['username']);
            sessionStorage.setItem('token', data['token']);
            sessionStorage.setItem('id', data['id']);
            this.router.navigate(['classroom']);
            this.username=sessionStorage.getItem('username');
            this.authOptions = {
                headers: new HttpHeaders({'Content-Type': 'application/json', 'Authorization': 'JWT ' + data['token']})
            };
        },
        err => {
            if (err['status'] === 400) {
              this.message = 'Login Failed: Invalid Credentials.';
            } else {
              this.message = 'Login Failed! Unexpected Error!';
            console.error(err);
            this.login_username = '';
            this.login_password = '';
            }
        }
    );
  }

  static islogin() {
      return !!sessionStorage.getItem('token');
  }

  logout() {
    this.username = '';

    sessionStorage.removeItem('username');
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('id');
    window.location.replace(environment.API_URL)
  }

  sessionSet(token:string,group_id:string) {
    this.http.post(environment.API_URL + 'sso_api/confirm_key',JSON.stringify({'token':token}),this.httpOptions).subscribe(data=>{
      sessionStorage.clear();
      sessionStorage.setItem('username', data['username']);
      sessionStorage.setItem('token', data['token']);
      sessionStorage.setItem('role', data['role']);
      sessionStorage.setItem('user_id', data['id']);
      alert('Signed in! Moving to class');
      this.router.navigate(['/classroom',group_id]);
      return true;

    },error => {
      console.log(error);
      return false;

    })

  }
}

