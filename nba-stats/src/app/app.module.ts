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

// COMPONENTS
import { NavigationComponent } from './navigation/toolbar/navigation.component';
import { SettingsComponent } from './sections/settings/settings.component';
import { SidenavComponent } from './navigation/sidenav/sidenav.component';
import { LoginDialogComponent } from './login/login.component';
import { PlayersComponent } from './sections/players/players.component';
import { TeamsComponent } from './sections/teams/teams.component';
import { DashboardComponent } from './sections/dashboard/dashboard.component';
import { TableComponent } from './shared/components/table/table.component';
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
    SettingsComponent,
    MapComponent,
    SidenavComponent,
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
    DashboardComponent,
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
