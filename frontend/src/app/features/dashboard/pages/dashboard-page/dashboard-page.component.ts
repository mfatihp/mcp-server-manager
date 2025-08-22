import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatsCardComponent } from '../../components/stats-card/stats-card.component';

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [CommonModule, StatsCardComponent],
  templateUrl: './dashboard-page.component.html'
})
export class DashboardPageComponent {
  stats = [
    { title: 'Tools Registered', value: 45, icon: '🛠️' },
    { title: 'Running Agents', value: 12, icon: '🤖' },
    { title: 'Errors Today', value: 3, icon: '⚠️' }
  ];
}
