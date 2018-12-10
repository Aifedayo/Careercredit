import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LinuxChatComponent } from './linux-chat.component';

describe('LinuxChatComponent', () => {
  let component: LinuxChatComponent;
  let fixture: ComponentFixture<LinuxChatComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LinuxChatComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LinuxChatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
