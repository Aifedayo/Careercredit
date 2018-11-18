export class Topic {
  public id: number;
  public title: string;
  public videoPath: string;

  constructor(id: number, title: string, videoPath: string) {
    this.id = id;
    this.title = title;
    this.videoPath = videoPath;
  }
}
