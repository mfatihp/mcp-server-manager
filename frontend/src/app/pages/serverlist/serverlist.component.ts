import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ServerCreateComponent } from './components/servercreate/servercreate.component';
import { ServerlistService } from './serverlist.service';
import { ServerItem } from './models/server-item.model';

@Component({
  selector: 'app-serverlist',
  standalone: true,
  imports: [CommonModule, FormsModule, ServerCreateComponent],
  templateUrl: './serverlist.component.html'
})

export class ServerlistComponent implements OnInit {
  constructor(private service: ServerlistService) {}

  servers: ServerItem[] = [];

  ngOnInit(): void {
    this.service.getServers();
    this.service.servers$.subscribe(data => {
      this.servers = data;
    });
  }


  showCreateModal = false;

  pauseServer(server: ServerItem) {
    if (server.IsRunning == false) {
      this.service.pauseMCPServer(server);
    } else {
      this.service.runMCPServer(server);
    }
  }
  
  deleteServer(server: ServerItem) { 
    this.service.deleteMCPServer(server); // TODO: Container işlemlerinin tamamlanması gerekiyor. arg olarak contID olacak.
  }

  addServer(server: ServerItem) {
    // Initialize pending state before sending request
    server.pending = true;
    server.IsRunning = false;

    this.service.addMCPServer(server);
  }

  // Search and filter
  searchText = '';

  get filteredServers() {
    if (!this.searchText) return this.servers;
    
    const lower = this.searchText.toLowerCase();
    
    return this.servers.filter(server =>
      server.name.toLowerCase().includes(lower) ||
      server.description.toLowerCase().includes(lower)
    );
  }
}
