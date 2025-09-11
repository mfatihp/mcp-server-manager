import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ServerlistService {

  private mcpCreateUrl = 'http://localhost:8000/manager/create_mcp_server';
  private mcpControlUrl = 'http://localhost:8000/manager/control_mcp_server';

  constructor(private http: HttpClient) { }

  servers = [
    { name: 'Server 1', description: 'First server', image: '/resource.png' },
    { name: 'Server 2', description: 'Second server', image: '/tool.png' }
  ];

  pauseServer(index: number) { 
    alert(`Paused: ${this.servers[index].name}`);

    this.http.post(this.mcpControlUrl, {}); // TODO: Create message body
  }
  
  deleteServer(index: number) { 
    this.servers.splice(index, 1); 

    this.http.post(this.mcpControlUrl, {}); // TODO: Create message body
  }
  
  editServer(index: number) { 
    alert(`Edit: ${this.servers[index].name}`); 
  }

  addServer(server: { name: string; description: string; serverType: string; image: string}) {
    this.servers.push({ ...server });

    this.http.post(this.mcpCreateUrl, {}); // TODO: Create message body
  }
}
