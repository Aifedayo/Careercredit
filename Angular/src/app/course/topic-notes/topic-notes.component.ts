import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {ApiService} from "../../share/api.service";

@Component({
  selector: 'app-topic-notes',
  templateUrl: './topic-notes.component.html',
  styleUrls: ['./topic-notes.component.css']
})
export class TopicNotesComponent implements OnInit {

 route:any ;
  public data$: any;
  constructor(
    private apiService:ApiService,route:ActivatedRoute,
    private router:Router,
    private cdr:ChangeDetectorRef) {
    this.route=route;
 this.data$=this.apiService.data$

  }
  ngOnInit() {

    // this.route.params.subscribe(params => {
    //   const selectedClass = + params["group_id"];
    // if (selectedClass){
    //   // this.apiService.LoadData(selectedClass);
    // this.apiService.setActiveTopic(+params["topic_id"]);
    //    }
    // });
    //
    //

  }

}
