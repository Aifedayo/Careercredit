import { Injectable } from '@angular/core';
import {CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot, ActivatedRoute} from '@angular/router';
import { Observable } from 'rxjs';
import { DataService } from './data.service';
import has = Reflect.has;
import {environment} from "../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  _hash:string;


  constructor(private dataservice: DataService, private router: Router) {  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot)
    : Observable<boolean> | Promise<boolean> | boolean {
      if (DataService.islogin()) {
        return true;
      }
      else {
        const hash = route.queryParamMap.get('hash');
        if (hash){
          const group_id=route.params['group_id'];
          console.log(group_id)
          if(this.dataservice.sessionSet(hash,group_id))
          return true

        }
        else{
          alert("Session expired, redirecting back to linuxjobber")
          window.location.replace(environment.API_URL);
          return false;
        }

      }
  }

}

