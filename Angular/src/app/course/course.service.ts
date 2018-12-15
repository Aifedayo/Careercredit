import { Topic } from './topic.model';
import { Injectable } from '@angular/core';
import {ApiService} from "../share/api.service";
import {CourseTopicModel} from "../share/course-topic-model";
import {Observable} from "rxjs/index";

@Injectable({
  providedIn: 'root'
})
export class CourseService {

  all_topics=[]
  public course_details:Observable<any[]>
  constructor(private apiService: ApiService){
    this.apiService.getCourseDetails(1)
      .subscribe(res=>{
        res['topics'].forEach(entry=>{
          let topic = new CourseTopicModel()
        topic.id=entry.id;
        topic.note= entry.note;
        topic.video=entry.video;
        topic.tasks=entry.tasks;
        this.all_topics.push(topic);
        })
      });
    console.log(this.all_topics)
  }
private topics: Topic [] = [
  new Topic (1, 'Django Definition and Installation', '/src/assets/videos/connect_sqlite.mp4'),
  new Topic (2, 'Creating Your First Django Project and Your First Django Application', '/assets/videos/connect_sqlite.mp4'),
  new Topic (3, 'Connecting With SQLlite, the Default Django Database System', ''),
  new Topic (4, 'Connecting Your Django Application to MySQL Database', ''),
  new Topic (5, 'Setting Up Django Administrator', ''),
  new Topic (6, 'Making Your Django Apps Reusable for Other Projects', ''),
  new Topic (7, 'Creating DJango Views', ''),
  new Topic (8, 'Using Django to Access and Manipulate Data in the Database', ''),
  new Topic (9, 'More on Using Django API to Edit Data in Database', ''),
  new Topic (10, 'Creating Django Views that Accept Arguments', ''),
  new Topic (11, 'Creating Views that Access the Database', ''),
  new Topic (12, 'Setting Up a Django Template', ''),
  // new Topic (13, 'Working with Django Models', ''),
  new Topic (14, 'Managing Error Messages Such as Page Not Found Error 404', ''),
  new Topic (15, 'Using Django API to Access Foreign Keys in Database Within a Template', ''),
  new Topic (16, 'Removing hardcoded URLs and namespacing URLs', ''),
  new Topic (17, 'Creating Forms in Templates', ''),
  new Topic (18, 'Submitting and Displaying Form Results', ''),
  new Topic (19, 'Using Generic Views to Display Django Webpages', ''),
  new Topic (20, 'Adding CSS, Cascading Stylesheets, to Django Templates', '')
];


getTopics() {
  // return this.topics.slice();
  return this.all_topics.slice();
  }
// getSingleTopic(index: number) {
//   return this.topics[index];
//   }
getSingleTopic(id: number) {
  const topic = this.all_topics.find(
    (data) => {
      return data.id === id;
    }
  );
  return topic;
}
}
