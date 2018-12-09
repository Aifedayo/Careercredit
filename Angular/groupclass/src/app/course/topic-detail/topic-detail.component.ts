import { CourseService } from './../course.service';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Topic } from '../topic.model';

@Component({
  selector: 'app-topic-detail',
  templateUrl: './topic-detail.component.html',
  styleUrls: ['./topic-detail.component.css']
})
export class TopicDetailComponent implements OnInit {
  public topics: Array<object> = [];
  topic: Topic;
  // id: number;
  // title: string;
  // videoPath: string;
  constructor(private route: ActivatedRoute, private courseService: CourseService) { }

  ngOnInit() {
    console.log('here')
    this.topics = this.courseService.getTopics();
    this.route.params.subscribe((params: Params) => {
      this.topic = this.courseService.getSingleTopic(+params['id']);
    });
  }

}
