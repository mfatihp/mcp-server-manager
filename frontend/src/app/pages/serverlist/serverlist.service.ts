import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ServerlistService {

  private mcpCreateUrl = 'http://localhost:8000/manager/create_mcp_server';
  private mcpControlUrl = 'http://localhost:8000/manager/control_mcp_server';
  private mcpCheckListUrl = 'http://localhost:8000/manager/check_list';

  constructor(private http: HttpClient) { }

  // TODO: Create empty list and schema for items
  // servers!: { name: string, description: string, image: string}[];
  servers = [
    { name: 'Server 1', description: 'First server', image: '/resource.png' },
    { name: 'Server 2', description: 'Second server', image: '/tool.png' }
  ];

  getServers() {
    this.http.get(this.mcpCheckListUrl, {});
    return this.servers;
  }

  pauseMCPServer(index: number, body: string) { 
    alert(`Paused: ${this.servers[index].name}`);

    this.http.post(this.mcpControlUrl, {
      serverId: "",
      controlCommand: "pause"
    });
  }
  
  deleteMCPServer(index: number) { 
    this.servers.splice(index, 1); 

    this.http.post(this.mcpControlUrl, {
      serverId: "",
      controlCommand: "delete"
    });
  }
  
  editMCPServer(index: number) { 
    alert(`Edit: ${this.servers[index].name}`);

    this.http.post(this.mcpControlUrl, {
      serverId: "",
      controlCommand: "edit",
      controlParams: {
          server_name: "",
          description: "",
          func: "",
          servertype: ""
      }
    });    
  }

  addMCPServer(server: { name: string; description: string; serverType: string; image: string}) {
    console.log("Frontend")
    // this.servers.push({ ...server });

    // Request doğru çalışmıyor. 
    this.http.post(this.mcpCreateUrl, server).subscribe(response => {
      console.log("Success:", response);},
      error => {
        console.log("Error:", error);
    });
  }
}
