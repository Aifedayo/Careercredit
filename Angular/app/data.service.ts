import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders} from '@angular/common/http';
import { Router} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  public URL = '54.244.162.68:8001';
  // public URL = '127.0.0.1:8000';

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

  // groupclassusers() {
  //     return this.http.get('http://' + this.URL + '/api/v1/groupclass-api/groupclassusers/');
  // }
  djangostudents() {
    return this.http.get('http://' + this.URL + '/classroom/djangostudent-api/djangostudent/');
  }
  // studentArray() {
  //   this.users [];
  //   this.djangostudents().subscribe((data: Array<object>) => {
  //     this.users = data;
  //     return this.users;
  //   });
  // }
  // getSingleStudent(id: number) {
  //   const user = this.users.find(
  //     (data) => {
  //       return data.id === id;
  //       console.log(data);
  //     }
  //   );
  //   return user;
  // }
  createUser() {
    this.http.post('http://' + this.URL + '/classroom/djangostudent-api/djangostudent/', JSON.stringify({'email': this.createuser_email, 'password': this.createuser_password, 'username': this.createuser_username}), this.httpOptions).subscribe(
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
    this.http.post('http://' + this.URL + '/classroom/api-token-auth/', JSON.stringify({'username': this.login_username, 'password': this.login_password}), this.httpOptions).subscribe(
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

