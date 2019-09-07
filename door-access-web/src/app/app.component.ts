import { Component } from '@angular/core';
import { DoorAjarService } from './services/door-ajar.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  public title = 'door-access-web';
  public serviceInFlight: boolean = false;
  public isError: boolean = false;
  public key: string = null;
  public message: string;

  constructor(private doorAjarSvc: DoorAjarService, private route: ActivatedRoute) {
    this.route.queryParams.subscribe(params => {
      this.key = params['doorkey'];
      if (!this.key) {
        this.isError = true;
        this.message = "No Key Provided. Please Request a new link.";
      } else {
        this.isError = false;
        this.message = "PLEASE do not press the button until you are in-front of the gate and ready to enter! When you have arrived at the gate, Press the button above to open it.";
        // Send Wakeup
        this.attemptOpen(true);
      }
    });
  }

  // constructor(private doorAjarSvc: DoorAjarService) { };
  // c5926552bec6fdd7ebfdbdc2a0d5ec5c8f0f17047e9578b908ec5be7
  attemptOpen(wake: Boolean = false) {
    this.serviceInFlight = true;
    this.isError = false

    if (wake) {
      this.message = "Waking Up Door Function. May Take a Min"
    } else {
      this.message = "Opening the door for you now, give it just a second!"
    }

    this.doorAjarSvc.openSesame(this.key, wake).subscribe((res: any) => {
      this.serviceInFlight = false;
      if (wake) {
        this.message = "PLEASE do not press the button until you are in-front of the gate and ready to enter! When you have arrived at the gate, Press the button above to open it.";

      } else {
        this.message = "Success! If the door isn't opening then something has gone wrong and it's not on your end!";
      }
    }, (err: any) => {
      this.serviceInFlight = false;
      this.isError = true;

      // Invalid Key
      if (err.status === 401) {
        this.message = "Key is invalid! Maybe it has expired?";
        if (err && err.error && err.error.msg) {
          this.message = this.message + " Message from server: " + err.error.msg;
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



