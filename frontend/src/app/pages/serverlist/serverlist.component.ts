import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ServerCreateComponent } from './components/servercreate/servercreate.component';
import { ServerlistService } from './serverlist.service';

@Component({
  selector: 'app-serverlist',
  standalone: true,
  imports: [CommonModule, FormsModule, ServerCreateComponent],
  templateUrl: './serverlist.component.html'
})

export class ServerlistComponent {
  constructor(private listservice: ServerlistService) {}

  showCreateModal = false;

  // Search and filter
  searchText = '';

  get filteredServers() {
    if (!this.searchText) return this.listservice;
    
    const lower = this.searchText.toLowerCase();
    
    return this.listservice.servers.filter(server =>
      server.name.toLowerCase().includes(lower) ||
      server.description.toLowerCase().includes(lower)
    );
  }
}
