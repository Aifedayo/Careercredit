import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {ApiService} from "../../share/api.service";
import {ActivatedRoute, Router} from "@angular/router";
import {Observable} from "rxjs/index";

@Component({
  selector: 'app-topic-lab',
  templateUrl: './topic-lab.component.html',
  styleUrls: ['./topic-lab.component.css']
})
export class TopicLabComponent implements OnInit {
  route:any ;
  public labs:any;
  constructor(private apiService:ApiService,route:ActivatedRoute,
              private router:Router) {
   this.labs=this.apiService.getLabs(sessionStorage.getItem('active_topic'))
  }
  ngOnInit() {

  }

}
