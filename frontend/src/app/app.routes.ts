import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ServerlistComponent } from './pages/serverlist/serverlist.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { MainLayoutComponent } from './layout/main-layout/main-layout.component';
import { LlmchatComponent } from './pages/llmchat/llmchat.component';


export const routes: Routes = [
  {
  path: '',
  component: MainLayoutComponent,
  children: [
    { path: '', component: HomeComponent },
    { path: 'servers', component: ServerlistComponent},
    { path: 'dashboard', component: DashboardComponent},
    { path: 'chat', component: LlmchatComponent}
  ]}
];