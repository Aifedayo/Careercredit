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
  public _task:Observable<any>;
  constructor(private apiService:ApiService,route:ActivatedRoute,
              private router:Router,
              private cdr:ChangeDetectorRef) {
    this.route=route;


  }
  ngOnInit() {
            this.route.params.subscribe(params => {

              this.cdr.reattach()
    this._task=this.apiService.data$
        });

  }

}
