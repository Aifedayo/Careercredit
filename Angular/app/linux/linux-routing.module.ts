import { LinuxChatComponent } from './linux-chat/linux-chat.component';
import { LinuxComponent } from './linux.component';
import { NgModule } from '@angular/core';

import { BrowserModule } from '@angular/platform-browser';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from '../auth.guard';

const linuxRoutes: Routes = [

  {
    path: 'linux',
    component: LinuxComponent, canActivate: [AuthGuard],

    children: [
      {
        path: '',

        children: [
          { path: 'linux-chat', component: LinuxChatComponent },
        ]
      }
    ]
  }
];

@NgModule({
  imports: [
    BrowserModule,
    RouterModule.forChild(linuxRoutes)
  ],
  declarations: [],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class LinuxRoutingModule { }
