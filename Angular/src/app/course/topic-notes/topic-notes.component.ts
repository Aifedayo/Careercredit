import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {ApiService} from "../../share/api.service";

@Component({
  selector: 'app-topic-notes',
  templateUrl: './topic-notes.component.html',
  styleUrls: ['./topic-notes.component.css']
})
export class TopicNotesComponent implements OnInit {

  note$:any
 route:any ;
  public data$: any;
  constructor(
    private apiService:ApiService,route:ActivatedRoute,
    private router:Router,) {
    this.note$=this.apiService.getNotes(sessionStorage.getItem('active_topic'))

  }
  ngOnInit() {





  }

}
