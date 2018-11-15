import { LinuxModule } from './linux.module';

describe('LinuxModule', () => {
  let linuxModule: LinuxModule;

  beforeEach(() => {
    linuxModule = new LinuxModule();
  });

  it('should create an instance', () => {
    expect(linuxModule).toBeTruthy();
  });
});
