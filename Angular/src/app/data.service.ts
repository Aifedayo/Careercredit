import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { Router} from '@angular/router';
import {environment} from "../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class DataService {

  // public URL = '54.244.162.68:8001';

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

  constructor(private http: HttpClient, private router: Router) { }

  createUser() {
    this.http.post('http://' + environment.API_URL + '/sso_api/login', JSON.stringify({'email': this.createuser_email, 'password': this.createuser_password, 'username': this.createuser_username}), this.httpOptions).subscribe(
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
    this.http.post('http://' + environment.API_URL + '/sso_api/api-token-auth/', JSON.stringify({'username': this.login_username, 'password': this.login_password}), this.httpOptions).subscribe(
        data => {

            sessionStorage.setItem('username', data['name']);
            sessionStorage.setItem('token', data['token']);
            sessionStorage.setItem('id', data['id']);
            this.username = this.login_username;
            this.router.navigate(['classroom']);
            this.login_username = '';
            this.login_password = '';
            this.id = '';
            console.log(this.username);
            console.log(this.id);

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

  islogin() {
      return !!sessionStorage.getItem('token');
  }

  logout() {
    this.username = '';
    this.router.navigate(['login']);
    sessionStorage.removeItem('username');
    sessionStorage.removeItem('token');
    sessionStorage.removeItem('id');
  }
}

