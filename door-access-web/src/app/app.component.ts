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
  // c5926552bec6fdd7ebfdbdc2a0d5ec5c8f0f17047e9578b908ec5be7
  attemptOpen() {
    console.log("TEST");
    this.doorAjarSvc.openSesame("c5926552bec6fdd7ebfdbdc2a0d5ec5c8f0f17047e9578b908ec5be7").subscribe((data: any) => {
      console.log("SUCCESS");
    });

  }
}



