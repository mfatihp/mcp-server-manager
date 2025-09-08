import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ServerlistComponent } from './pages/serverlist/serverlist.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'servers', component: ServerlistComponent},
  { path: 'dashboard', component: DashboardComponent},
];