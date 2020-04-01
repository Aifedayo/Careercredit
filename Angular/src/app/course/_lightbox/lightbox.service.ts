import { Injectable } from '@angular/core';
import { Observable, of, Subject } from 'rxjs';
import { images } from './lightbox.model';

@Injectable({ providedIn: 'root' })
export class LightboxService {

  setGroupFilter$ = new Subject<any>();
  getGroupFilter = this.setGroupFilter$.asObservable();

  constructor() {}

  fetchImages(): Observable<any> {
    return of(images);
  }
}