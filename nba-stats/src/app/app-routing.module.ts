import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { PlayersComponent } from './sections/players/players.component';
import { TeamsComponent } from './sections/teams/teams.component';
import { DashboardComponent } from './sections/dashboard/dashboard.component';
import { PlayerComponent } from './sections/player/player.component';
import { TeamComponent } from './sections/team/team.component';
import { PageNotFoundComponent } from './navigation/page-not-found/page-not-found.component';
import { AuthGuard } from './shared/guards/auth.guard';
import { AdminComponent } from './sections/admin/admin.component';


const routes: Routes = [
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
    path: 'dashboard',
    component: DashboardComponent,
    canActivate: [AuthGuard],
    data: {level: null}
  },
  {
    path: 'admin',
    component: AdminComponent,
    canActivate: [AuthGuard],
    data: {level: 'admin'}
  },
  {
    path: 'players',
    component: PlayersComponent,
    canActivate: [AuthGuard],
    data: {level: null}
  },
  {
    path: 'players/:id',
    component: PlayerComponent,
    canActivate: [AuthGuard],
    data: {level: 'authenticated'}
  },
  {
    path: 'teams',
    component: TeamsComponent,
    canActivate: [AuthGuard],
    data: {level: null}
  },
  {
    path: 'teams/:id',
    component: TeamComponent,
    canActivate: [AuthGuard],
    data: {level: 'authenticated'}
  },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
