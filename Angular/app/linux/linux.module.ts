import { NgModule } from '@angular/core';
import { LinuxChatComponent } from './linux-chat/linux-chat.component';
import { BrowserModule} from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatVideoModule } from 'mat-video';
import { MaterializeModule } from 'angular2-materialize';
import { LinuxComponent } from './linux.component';
import { LinuxRoutingModule } from './linux-routing.module';



@NgModule({
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatVideoModule,
    MaterializeModule,
    LinuxRoutingModule
  ],
  declarations: [
    LinuxChatComponent,
    LinuxComponent
  ],
  bootstrap: [LinuxComponent]
})
export class LinuxModule { }
