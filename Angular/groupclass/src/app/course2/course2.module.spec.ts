import { Course2Module } from './course2.module';

describe('Course2Module', () => {
  let course2Module: Course2Module;

  beforeEach(() => {
    course2Module = new Course2Module();
  });

  it('should create an instance', () => {
    expect(course2Module).toBeTruthy();
  });
});
