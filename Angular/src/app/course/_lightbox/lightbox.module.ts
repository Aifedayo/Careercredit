import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LightboxComponent } from './lightbox.component';

@NgModule({
    imports: [CommonModule],
    declarations: [LightboxComponent],
    exports: [LightboxComponent]
})
export class LightboxModule { }