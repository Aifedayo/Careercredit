import { Component, OnInit } from '@angular/core';
import {ApiService} from "../../share/api.service";
import {Observable} from "rxjs/index";
import {ClassModel} from "../../share/class-model";

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.css']
})
export class SettingsComponent implements OnInit {

  group=new ClassModel();
  constructor(private apiService:ApiService) {
     this.apiService.getGroupInfo(sessionStorage.getItem('active_group')).subscribe(res=>{
      this.group.video_required=res['video_required'];
      this.group.id=res['id'];
    })
  }

  ngOnInit() {


  }

  toggleVideo(){
    this.group.video_required = !(!this.group.video_required);
    this.apiService.updateGroupInfo(this.group).subscribe(res=>{

    })
  }

}
