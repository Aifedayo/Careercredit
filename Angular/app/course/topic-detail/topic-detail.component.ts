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
    this.topics = this.courseService.getTopics();
    this.topic = {
      id: +this.route.snapshot.params['id'],
      title: this.route.snapshot.params['title'],
      videoPath: this.route.snapshot.params['videoPath']
    };
    this.route.params.subscribe((params: Params) => {
      this.topic = this.courseService.getSingleTopic(+params['id']);
    });
  }

}
