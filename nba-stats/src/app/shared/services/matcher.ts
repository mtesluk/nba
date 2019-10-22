import { ErrorStateMatcher as Err } from '@angular/material';
import { FormControl, FormGroupDirective, NgForm } from '@angular/forms';


export class ErrorStateMatcher implements Err {
    isErrorState(control: FormControl | null, form: FormGroupDirective | NgForm | null): boolean {
      const isSubmitted = form && form.submitted;
      return !!(control && control.invalid && (control.dirty || control.touched || isSubmitted));
    }
}
