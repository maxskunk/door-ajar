import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { retry, catchError, tap } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class DoorAjarService {

  // Define API
  apiURL = "https://us-central1-zokya-media.cloudfunctions.net/dooraccess";

  //https://us-central1-zokya-media.cloudfunctions.net/dooraccess?key=c5926552bec6fdd7ebfdbdc2a0d5ec5c8f0f17047e9578b908ec5be7&wakeup=True

  constructor(private http: HttpClient) { }

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  }

  // HttpClient API get() method => Fetch employee
  openSesame(key, wakeup: Boolean = false): Observable<any> {
    const wakeup_value = wakeup ? "True" : "False";
    let params = new HttpParams();
    params = params.append('key', key);
    params = params.append('wakeup', wakeup_value);
    return this.http.get<any>(this.apiURL, { params: params }).pipe(
      tap( // Log the result or error
        data => {
          return data;
        },
        error => {
          return error;
        }
      )
    )
  }

  // Error handling 
  handleError(error) {
    let errorMessage = '';
    if (error.error instanceof ErrorEvent) {
      // Get client-side error
      errorMessage = error.error.message;
    } else {
      // Get server-side error
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
    }
    return throwError(errorMessage);
  }

}
