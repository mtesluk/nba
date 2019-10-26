import { Component, OnInit, ViewChild, Input, AfterViewInit } from '@angular/core';
import { MatPaginator, MatSort } from '@angular/material';
import { TableService } from './table.service';
import { merge, of, Subject } from 'rxjs';
import { startWith, switchMap, map, catchError, debounceTime } from 'rxjs/operators';
import { NgForm } from '@angular/forms';
import { URLS } from 'src/environments/environment';
import { Router, RouterModule } from '@angular/router';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';
import { NotifyService } from '../../services/notify.service';
import { AuthService } from '../../services/auth.service';


@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.scss'],
  providers: [
    TableService,
  ]
})
export class TableComponent implements OnInit, AfterViewInit {

  @Input() set filters(value) {
    this._filters = {...this._filters, ...value};
    this.isLoadedFirstTime = true;
    this._filterState$.next();
  }
  get filters() {
    return this._filters;
  }
  @Input() namesToFilter = [];
  @Input() namesToSort = [];
  @Input() initSorting = '';
  @Input() endpoint = null;
  @Input() excludeColumns = [];
  @Input() compare = false;
  @Input() maxPageSize = 10;
  @Input() showPaginator = true;
  @Input() title = '';
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild('form') form: NgForm;
  resultsLength = 0;
  isLoading = true;
  data: [] = [];
  inputs = {};
  isLoadedFirstTime = false;
  additionalColumns: string[] = [];
  displayedColumns: string[] = [];
  displayedColumnsWithSelect: string[] = [];
  hints: {} = {};
  dataCompare = [];
  dataBet: Set<string> = new Set();
  private _filterState$ = new Subject<null>();
  private _filters = {};

  constructor(private _service: TableService,
              private _router: Router,
              private _notificationService: NotifyService,
              private _authService: AuthService,
            ) { }

  ngOnInit() {

  }

  ngAfterViewInit() {
    this.sort.sortChange.subscribe(() => this.paginator.pageIndex = 0);
    this._setupHints();
    this._setupDataSubscriber();
  }

  _setupDataSubscriber() {
    merge(this.sort.sortChange, this.paginator.page, this.form.valueChanges, this._filterState$)
      .pipe(
        debounceTime(500),
        startWith({}),
        switchMap(() => {
          this.isLoading = true;
          this._filters = {...this.filters, ...this.form.value};
          if (this.initSorting.length > 0) {
            this._filters['ordering'] = this.initSorting;
          }
          if (this.sort.active !== undefined) {
            this._filters['ordering'] = this.sort.direction === 'asc' ? this.sort.active : `-${this.sort.active}`;
          }
          this._filters['page'] = this.paginator.pageIndex + 1;
          this._filters['page_size'] = this.maxPageSize;
          return this._service.getData(this.endpoint, this.filters);
        }),
        map(response => {
          this.resultsLength = response.count;
          return response.results;
        }),
        map(results => {
          results = results.map(value => {
            const stats = value.stats;
            if (Object.keys(stats).length !== 0) {
              this.additionalColumns = Object.keys(stats);
            } else {
              return {};
            }
            delete value.stats;
            this.displayedColumns  = Object.keys(value).concat(this.additionalColumns);
            this.displayedColumns = this.displayedColumns.filter(elem => !this.excludeColumns.includes(elem));
            if (this.compare) {
              this.displayedColumns.push('selectCompare')
            }
            return {...value, ...stats};
          });
          this.isLoading = false;
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
      this.data = data.filter(elem => Object.keys(elem).length > 0);
    }
  }

  _setupHints() {
    this._service.getHints(this.endpoint + URLS['hint']).subscribe(response => {
      this.hints = response.reduce((result, element) => {
        result[element['name']] = element['hint'];
        return result;
      }, {});
    });
  }

  includedIn(column: string) {
    return this.namesToSort.includes(column);
  }

  navigateTo(value: string) {
    this._router.navigate([this.title, value]);
  }

  addToCompare(row) {
    this.dataCompare = Array.from(this.dataCompare.concat(row));
  }

  addToBet(row) {
    if (this.dataBet.size >= 5) {
      this._notificationService.notify('You have already 5 elements to bet, remove if you wanna change');
    } else {
      this.dataBet = this.dataBet.add(row['name']);
    }
  }

  bet() {
    if (!this._authService.isAuthenticated()) {
      this._notificationService.notify('You have no right to bet, sign up or sign in to participate in this action');
    } else {
      
    }
  }

  removeBet(row: string) {
    this.dataBet.forEach(name => {
      if (name === row) {
        this.dataBet.delete(row);
      }
    });
  }

  drop(event: CdkDragDrop<string[]>) {
    moveItemInArray(Array.from(this.dataBet), event.previousIndex, event.currentIndex);
  }
}
