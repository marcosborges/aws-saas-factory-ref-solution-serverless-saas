/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs';
import { map, switchMap } from 'rxjs/operators';
import { Plan } from '../models/plan.interface';
import { PlanService } from '../plan.service';

@Component({
  selector: 'app-plan-edit',
  templateUrl: './plan-edit.component.html',
  styles: [
  ]
})
export class PlanEditComponent implements OnInit {

  constructor(private route: ActivatedRoute,
              private router: Router,
              private planSvc: PlanService,
              private fb: FormBuilder) { }
  planForm: FormGroup;
  plan$: Observable<Plan>;
  key$: Observable<string>;
  files: File[];


  ngOnInit(): void {
    this.key$ = this.route.params.pipe(
      map(p => p.key)
    );

    this.plan$ = this.key$.pipe(
      switchMap(p => this.planSvc.get(p))
    );

    this.planForm = this.fb.group({
      key: [''],
      planId: [''],
      name: [''],
      price: [''],
      sku: [''],
      category:['']
    });

    // Is this right? Seems like I should be able to feed the form an observable
    this.plan$.subscribe(val => {
      this.planForm.patchValue({
        ...val
      });

    });

  }

  submit() {
    this.planSvc.put(this.planForm.value).subscribe(() => {
      this.router.navigate(['plans']);
    }, (err) => {
      alert(err);
      console.error(err);
    });
  }

  delete() {
    this.planSvc.delete(this.planForm.value).subscribe(() => {
      this.router.navigate(['plans']);
    }, (err) => {
      alert(err);
      console.error(err);
    });
  }

  cancel() {
    this.router.navigate(['plans']);
  }


}
