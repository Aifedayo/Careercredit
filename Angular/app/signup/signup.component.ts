import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  constructor(private router: Router, public dataservice: DataService) { }

  ngOnInit() {
  }

  toLogin()
  {
    this.router.navigate(['login']);
    
  }
  
  createUser()
  {
    this.dataservice.createUser();  
    this.dataservice.message = '';
  }

}
