import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
declare var moment: any;

@Component({
  selector: 'app-qoute-message',
  templateUrl: './qoute-message.component.html',
  styleUrls: ['./qoute-message.component.css'],
})
export class QouteMessageComponent implements OnInit {
    @Input() message = {};
    @Input() display_close:Boolean = false;
    @Output() closed = new EventEmitter();

    ngOnInit(): void {}  

    close(){
      this.closed.emit()
    }

    formatDate(timestamp){
      timestamp = timestamp.indexOf(':')== -1?timestamp:'1579454456729'
      return moment(Number(timestamp)).format('l');
    }
}