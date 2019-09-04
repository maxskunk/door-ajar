import { Component } from '@angular/core';
import { DoorAjarService } from './services/door-ajar.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  public title = 'door-access-web';
  public serviceInFlight: boolean = false;
  public isError: boolean = false;
  public message: string = "PLEASE do not press the button until you are in-front of the gate and ready to enter! When you have arrived at the gate, Press the button above to open it.";

  constructor(private doorAjarSvc: DoorAjarService) { };
  // c5926552bec6fdd7ebfdbdc2a0d5ec5c8f0f17047e9578b908ec5be7
  attemptOpen() {
    this.serviceInFlight = true;
    this.isError = false

    this.doorAjarSvc.openSesame("c5926552bec6fdd7ebfdbdc2a0d5ec5c8f0f17047e9578b908ec5be7").subscribe((res: any) => {
      this.serviceInFlight = false;
      this.message = "Success! If the door isn't opening then something has gone wrong and it's not on your end!";
    }, (err: any) => {
      this.serviceInFlight = false;
      this.isError = true;

      // Invalid Key
      if (err.status === 401) {
        this.message = "Key is invalid! Maybe you are early?";
        if (err && err.error && err.error.msg) {
          this.message = this.message + " " + err.error.msg;
        }
      } else if (err.status === 401) {
        this.message = "Looks Like There is An Invalid Key";
      } else if (err.status === 412) {
        this.message = "Your key is not valid yet! Are you early?";
      } else {
        this.message = "Something Unexpected has Happened";
      }
    });

  }
}



