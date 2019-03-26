import {
  Component,
  OnInit,
  OnDestroy,
  ElementRef,
  Input
} from '@angular/core';

import videojs from 'video.js';
import * as adapter from 'webrtc-adapter/out/adapter_no_global.js';
import * as RecordRTC from 'recordrtc';

// register videojs-record plugin with this import
import * as Record from 'videojs-record/dist/videojs.record.js';
import {environment} from "../../../environments/environment";
import {ApiService} from "../../share/api.service";
import {Router} from "@angular/router";

@Component({
  selector: 'videojs-record',
  templateUrl: './verification.component.html',
  styleUrls: ['./verification.component.css']
})

export class VerificationComponent implements OnInit, OnDestroy {

  // reference to the element itself: used to access events and methods
  private _elementRef: ElementRef;

  // index to create unique ID for component
  // @Input() idx: string;
  idx='1';
  private config: any;
  private player: any;
  private plugin: any;

  // constructor initializes our declared vars
  constructor(elementRef: ElementRef,private apiService:ApiService,private router:Router) {
    this.player = false;

    // save reference to plugin (so it initializes)
    this.plugin = Record;

    // video.js configuration
    this.config = {
      controls: true,
      autoplay: false,
      fluid: false,
      loop: false,
      width: 450,
      height: 400,
      controlBar: {
        volumePanel: false
      },
      plugins: {
        // configure videojs-record plugin
        record: {
          audio: false,
          video: true,
          debug: true
        }
      }
    };
  }

  ngOnInit() {}

  // use ngAfterViewInit to make sure we initialize the videojs element
  // after the component template itself has been rendered
  ngAfterViewInit() {
    // ID with which to access the template's video element
    let el = 'video_' + this.idx;

    // setup the player via the unique element ID
    this.player = videojs(document.getElementById(el), this.config, () => {
      console.log('player ready! id:', el);

      // print version information at startup
      var msg = 'Using video.js ' + videojs.VERSION +
        ' with videojs-record ' + videojs.getPluginVersion('record') +
        ' and recordrtc ' + RecordRTC.version;
      videojs.log(msg);
    });

    // device is ready
    this.player.on('deviceReady', () => {
      console.log('device is ready!');
    });

    // user clicked the record button and started recording
    this.player.on('startRecord', () => {
      console.log('started recording!');
    });

    // user completed recording and stream is available
    this.player.on('finishRecord', () => {
      // recordedData is a blob object containing the recorded data that
      // can be downloaded by the user, stored on server etc.
      console.log('finished recording: ', this.player.recordedData);
      this.uploadVideo(this.player.recordedData)
    });

    // error handling
    this.player.on('error', (element, error) => {
      console.warn(error);
    });

    this.player.on('deviceError', () => {
      console.error('device error:', this.player.deviceErrorCode);
    });
  }

  // use ngOnDestroy to detach event handlers and remove the player
  ngOnDestroy() {
    if (this.player) {
      this.player.dispose();
      this.player = false;
    }
  }

  uploadVideo(data): void {
            const formData = new FormData();
            formData.append('video', data, data.name);
            formData.append('active_group', sessionStorage.getItem('active_group'));

            this.apiService.uploadVideo(formData)
                 .subscribe(
                     data => {
                       const url= environment.API_URL + data['video_url'];
                       console.log(url)
                       this.router.navigate(['/classroom/'+sessionStorage.getItem('active_group')])
                     },
                     error => alert('Video not uploaded, try again')
                 );

    }

}
