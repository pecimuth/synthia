import { Component, Input, OnInit } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Component({
  selector: 'app-form-field',
  templateUrl: './form-field.component.html',
  styleUrls: ['./form-field.component.scss']
})
export class FormFieldComponent implements OnInit {

  @Input() form: FormGroup;
  @Input() label: string;
  @Input() name: string;
  @Input() type = 'text';
  @Input() placeholder: string = null;

  constructor() { }

  ngOnInit(): void {
  }

}
