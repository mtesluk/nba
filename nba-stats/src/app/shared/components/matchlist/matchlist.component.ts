import { MatchlistService } from './matchlist.service';
import { Component, OnInit, ViewChild, Input } from '@angular/core';
import { MatPaginator, MatSort } from '@angular/material';
import { merge, of, Subject } from 'rxjs';
import { startWith, switchMap, map, catchError, debounceTime } from 'rxjs/operators';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-matchlist',
  templateUrl: './matchlist.component.html',
  styleUrls: ['./matchlist.component.scss'],
  providers: [
    MatchlistService,
  ]
})
export class MatchlistComponent implements OnInit {

  @Input() set filters(value) {
    Object.keys(value).forEach(filterName => {
      if (value[filterName] !== this._filters[filterName]) {
        this.paginator._changePageSize(this.paginator.pageSize);
        this._filters[filterName] = value[filterName];
      }
    });
  }
  get filters() {
    return this._filters;
  }
  @Input() namesToFilter = [];
  @Input() endpoint = null;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild('form') form: NgForm;
  resultsLength = 0;
  isLoading = true;
  data: [] = [];
  inputs = {};
  private _filters = {};

  constructor(private _service: MatchlistService, private router: Router) { }

  onRowClicked(obj: any) {
    this.router.navigate(['../matches/', obj.id]);
  }

  ngOnInit() {
    this.sort.sortChange.subscribe(() => this.paginator.pageIndex = 0);

    merge(this.paginator.page, this.form.valueChanges)
      .pipe(
        debounceTime(500),
        startWith({}),
        switchMap(() => {
          this.isLoading = true;
          this.filters = {...this.filters, ...this.form.value};
          this.filters['page'] = this.paginator.pageIndex + 1;
          return this._service.getData(this.endpoint, this.filters);
        }),
        map(response => {
          this.isLoading = false;
          this.resultsLength = response.count;
          return response.results;
        }),
        map(results => {
          results = results.map(value => {
            const stats = value.stats;
            delete value.stats;
            return {...value, ...stats};
          });
          return results;
        }),
        catchError(() => {
          this.isLoading = false;
          return of([]);
        })
      ).subscribe(data => this._setupData(data));
  }

  _setupData(data) {
    if (data.length > 0) {
      this.data = data;
    }
  }
}
