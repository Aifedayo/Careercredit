import { 
    OnInit, OnDestroy, ViewChild, Output, 
    Input, ElementRef, EventEmitter, Component 
} from '@angular/core';

@Component({
    selector: 'infinite-scroll',
    template: `<div #anchor><ng-content></ng-content></div>`,
    // template: `<ng-content></ng-content><div #anchor></div>`,
  })
  export class InfiniteScrollComponent implements OnInit, OnDestroy {
    @Input() options = {};
    @Output() scrolled = new EventEmitter();
    @ViewChild('anchor') anchor: ElementRef<HTMLElement>;
  
    private observer: IntersectionObserver;
  
    constructor(private host: ElementRef) { }
  
    get element() {
      return this.host.nativeElement;
    }

    
    ngOnInit() {
        const options = {
            root: null,
            ...this.options
        };

        this.observer = new IntersectionObserver(([entry]) => {
            entry.isIntersecting && this.scrolled.emit();
        }, options);

        this.observer.observe(this.anchor.nativeElement);
    }

    private isHostScrollable() {
        const style = window.getComputedStyle(this.element);
    
        return style.getPropertyValue('overflow') === 'auto' ||
          style.getPropertyValue('overflow-y') === 'scroll';
    }

    ngOnDestroy() {
        this.observer.disconnect();
    }

  }