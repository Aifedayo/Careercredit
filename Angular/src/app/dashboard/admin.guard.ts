import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import {ApiService} from "../share/api.service";

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {
  private role:number = 3;
   constructor(private apiService:ApiService){
      this.apiService.getUserInfo().subscribe(res=>{
      this.role= res['role'];
    });
   }

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean
  {
      return sessionStorage.getItem('role') === this.role.toString();
  }
}
