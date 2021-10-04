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
import { NgModule, APP_INITIALIZER } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { PlansRoutingModule } from './plans-routing.module';
import { PlanListComponent } from './plan-list/plan-list.component';
import { PlanCreateComponent } from './plan-create/plan-create.component';
import { PlanEditComponent } from './plan-edit/plan-edit.component';

// 3P components
import { NgxDropzoneModule } from 'ngx-dropzone';
import { PopoverModule } from 'ngx-bootstrap/popover';

import { configureAuth } from '../views/auth/auth-config';
import { AuthConfigurationService } from '../views/auth/auth-configuration.service';


@NgModule({
  declarations: [PlanListComponent, PlanCreateComponent, PlanEditComponent],
  imports: [
    CommonModule,
    FormsModule,
    PopoverModule.forRoot(),
    PlansRoutingModule,
    ReactiveFormsModule,
    NgxDropzoneModule
  ]
})
export class PlansModule { }
