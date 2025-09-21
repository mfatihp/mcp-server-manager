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

  private func = "";

  mcp_schema!: {
    "server_name": string, 
    "description": string, 
    "func_args": string, 
    "func_body": string, 
    "servertype": string; 
    "pkgs": string[] 
  };

  constructor(private http: HttpClient) { }

  // TODO: Create empty list and schema for items !!!!IMPORTANT
  // servers!: { name: string, description: string, image: string}[];
  servers = [
    { name: 'Server 1', description: 'First server', image: '/resource.png' },
    { name: 'Server 2', description: 'Second server', image: '/tool.png' }
  ];

  getServers() {
    this.http.get(this.mcpCheckListUrl, {});
    return this.servers;
  }

  pauseMCPServer(index: number) { 
    alert(`Paused: ${this.servers[index].name}`);

    // TODO: subscribe kısmındaki uyarıya bakılacak
    this.http.post(this.mcpCreateUrl, {
                                        serverId: "",
                                        controlCommand: "pause"
                                      }).subscribe(response => {
                                                                console.log("Success:", response);},
                                                                error => {
                                                                  console.log("Error:", error);
                                                              });
  }
  
  deleteMCPServer(index: number) { 
    this.servers.splice(index, 1); 

    this.http.post(this.mcpControlUrl, {
      serverId: "",
      controlCommand: "delete"
    });
    // TODO: subscribe kısmındaki uyarıya bakılacak
    this.http.post(this.mcpCreateUrl, {
                                        serverId: "",
                                        controlCommand: "delete"
                                      }).subscribe(response => {
                                                                console.log("Success:", response);},
                                                                error => {
                                                                  console.log("Error:", error);
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

  addMCPServer(server: { name: string; 
                         description: string; 
                         serverType: string; 
                         image: string; 
                         pkgs: string[],
                         func_args: string,
                         func_body: string
                        }) {

    this.mcp_schema = {"server_name": server.name, 
                        "description": server.description,
                        "servertype": server.serverType,
                        "pkgs": server.pkgs,
                        "func_args": server.func_args, 
                        "func_body": server.func_body, 
                      }

    // TODO: subscribe kısmındaki uyarıya bakılacak
    this.http.post(this.mcpCreateUrl, this.mcp_schema).subscribe(response => {
                                                                              console.log("Success:", response);},
                                                                              error => {
                                                                                console.log("Error:", error);
                                                                            });
  }
}
