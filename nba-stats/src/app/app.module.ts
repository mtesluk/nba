import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { MaterialModule } from './material-module.module';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';
import { ReactiveFormsModule } from '@angular/forms';
// import { CookieService } from 'ngx-cookie';

// COMPONENTS
import { NavigationComponent } from './navigation/navigation.component';
import { LoginDialogComponent } from './login/login.component';
import { PlayersComponent } from './sections/players/players.component';
import { TeamsComponent } from './sections/teams/teams.component';
import { MatchesComponent } from './sections/matches/matches.component';
import { DashboardComponent } from './sections/dashboard/dashboard.component';
import { TableComponent } from './shared/components/table/table.component';
import { MatchlistComponent } from './shared/components/matchlist/matchlist.component';
import { MatchComponent } from './sections/match/match.component';
import { PlayerComponent } from './sections/player/player.component';
import { TeamComponent } from './sections/team/team.component';
import { StatsComponent } from './shared/components/stats/stats.component';
import { PageNotFoundComponent } from './navigation/page-not-found/page-not-found.component';
import { RegistrationDialogComponent } from './registration/registration.component';
import { MapComponent } from './shared/components/map/map.component';
import { AdminComponent } from './sections/admin/admin.component';
import { AdminActionDialogComponent } from './shared/components/admin-action-dialog/admin-action-dialog.component';

// SERVIECES
import { AuthService } from './shared/services/auth.service';

// GUARDS
import { AuthGuard } from './shared/guards/auth.guard';
import { AuthInterceptor } from './shared/interceptors/auth.interceptor';

@NgModule({
  declarations: [
    AdminComponent,
    TableComponent,
    MapComponent,
    PageNotFoundComponent,
    AppComponent,
    NavigationComponent,
    PlayersComponent,
    PlayerComponent,
    LoginDialogComponent,
    TeamsComponent,
    TeamComponent,
    RegistrationDialogComponent,
    AdminActionDialogComponent,
    StatsComponent,
    MatchesComponent,
    DashboardComponent,
    MatchlistComponent,
    MatchComponent,
  ],
  entryComponents: [
    LoginDialogComponent,
    AdminActionDialogComponent,
    RegistrationDialogComponent,
  ],
  imports: [
    BrowserModule,
    FlexLayoutModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MaterialModule,
    AppRoutingModule,
    ReactiveFormsModule,
    FormsModule,
  ],
  providers: [
    AuthService,
    AuthGuard,
    // CookieService
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
  },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
