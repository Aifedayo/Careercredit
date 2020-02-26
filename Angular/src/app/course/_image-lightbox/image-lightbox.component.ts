import {Input, Component, OnInit} from '@angular/core';


@Component({
  selector: 'app-image-lightbox',
  templateUrl: './image-lightbox.component.html',
  styleUrls: ['./image-lightbox.component.css']
})
export class ImageLightboxComponent implements OnInit {
  
  @Input() imageUrl;
  constructor() {}
  ngOnInit() {

  }

  openModal() {
    document.getElementById('lightboxModal').style.display = "block";
    document.getElementById('lightboxModalImg').setAttribute("src",this.imageUrl);
  }

  closeModal() {
    document.getElementById('lightboxModal').style.display = "none";
  }
}
