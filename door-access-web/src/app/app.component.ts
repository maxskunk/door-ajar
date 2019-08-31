import { Component } from '@angular/core';
import { DoorAjarService } from './services/door-ajar.service'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  public title = 'door-access-web';

  constructor(private doorAjarSvc: DoorAjarService) { };

  attemptOpen() {
    console.log("TEST");
    this.doorAjarSvc.openSesame("e223dc007d659adc8ddfcc67a1fc555c645dcec57ce691022df52f8c602504be").subscribe((data: any) => {
      console.log("SUCCESS");
    });

  }
}



