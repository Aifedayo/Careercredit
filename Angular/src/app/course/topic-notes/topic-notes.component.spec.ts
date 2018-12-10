import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TopicNotesComponent } from './topic-notes.component';

describe('TopicNotesComponent', () => {
  let component: TopicNotesComponent;
  let fixture: ComponentFixture<TopicNotesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TopicNotesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TopicNotesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
