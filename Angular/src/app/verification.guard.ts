import { Injectable } from '@angular/core';
import {CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router} from '@angular/router';
import { Observable } from 'rxjs';
import {ApiService} from "./share/api.service";
import {DataService} from "./data.service";
import {state} from "@angular/animations";

@Injectable({
  providedIn: 'root'
})
export class VerificationGuard implements CanActivate {

  private required: Observable<boolean> | Promise<boolean> | boolean=true;
  private uploaded: Observable<boolean> | Promise<boolean> | boolean=false;
  constructor(private apiService:ApiService, private router:Router){


  }

  goToClass(){
    // this.router.navigate()

  }
  goToVerification(){
    // this.router.navigate()

  }

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean
  {
    const group_id=next.params['group_id'];
        this.required = this.apiService.videoRequired(group_id);
      this.uploaded = this.apiService.videoUploded(group_id);
    if(!! this.required){
      if(!! this.uploaded){
        this.router.navigate(['/classroom/' + group_id])
        return true
      }
      else {
        this.router.navigate(['/v'] );
      }
    }
    else{
      this.router.navigate(['/classroom/' + group_id])
      return true
    }

  }
}


@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {

  private is_instructor: boolean;
  constructor(private dataservice:DataService, private router:Router){
  }

  canActivate() {
    // const group_id=next.params['group_id'];
    this.is_instructor = this.dataservice.isInstructor();
    if(this.is_instructor){
      console.log('hello')
      return true
    }
    else{
      // this.router.navigate(['/classroom/' + group_id])
      return false
    }

  }
}