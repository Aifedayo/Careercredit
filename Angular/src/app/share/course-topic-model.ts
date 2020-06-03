export class CourseTopicModel {
  id:number;
  topic: string;
  video:string;
  tasks=[];
  note:string;
  constructor(){

  }
}

export class EditTopicModel {
  id:number;
  topic: string;
  video:string;
  constructor(){
  }
}
