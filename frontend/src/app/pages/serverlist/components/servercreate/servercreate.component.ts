import { Component, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-server-create',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './servercreate.component.html'
})

export class ServerCreateComponent {
  @Output() serverCreated = new EventEmitter<{ name: string; 
                                               description: string; 
                                               serverType: string; 
                                               image: string; 
                                               pkgs: string[]; 
                                               func_body: string; 
                                               func_args: string; 
                                               pending: boolean }>();
  @Output() close = new EventEmitter<void>();

  newServerName = '';
  newServerDesc = '';
  schemaJson = '{\n  "description": "value"\n}';
  codeFunctionName = '';
  codeArgs = '';
  codeBody = '';
  servertype = '';
  serverpending = true;
  images: Record<string, string> = {
    tool: '/tool.png',
    resource: '/resource.png'
  };

  searchTerm = '';
  selectedPackages: string[] = [];

  examplePackages = [
    { name: "numpy", description: "Fundamental package for array computing in Python" },
    { name: "pandas", description: "Data analysis and manipulation tool" },
    { name: "requests", description: "HTTP library for Python" },
    { name: "matplotlib", description: "2D plotting library" },
    { name: "scikit-learn", description: "Machine learning in Python" }
  ];

  togglePackage(pkg: string) {
    if (this.selectedPackages.includes(pkg)) {
      this.selectedPackages = this.selectedPackages.filter(p => p !== pkg);
    } else {
      this.selectedPackages.push(pkg);
    }
  }

  isSelected(pkg: string): boolean {
    return this.selectedPackages.includes(pkg);
  }

  get filteredPackages() {
    return this.examplePackages.filter(p =>
      p.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  createServer() {
    if (!this.newServerName) return;
    this.serverCreated.emit({
      name: this.newServerName,
      description: this.newServerDesc,
      serverType: this.servertype,
      image: this.images[this.servertype],
      pkgs: this.selectedPackages,
      func_body:this.codeBody,
      func_args:this.codeArgs,
      pending:this.serverpending,
    });
    this.newServerName = '';
    this.newServerDesc = '';
  }

  cancel() {
    this.close.emit();
  }
}
