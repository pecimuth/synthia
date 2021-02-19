import { Component, Input, OnInit } from '@angular/core';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { ResourceService } from '../service/resource.service';

@Component({
  selector: 'app-resource',
  templateUrl: './resource.component.html',
  styleUrls: ['./resource.component.scss']
})
export class ResourceComponent implements OnInit {

  @Input() dataSource: DataSourceView;
  
  constructor(private resourceService: ResourceService) { }

  ngOnInit(): void {
  }

  import() {
    this.resourceService.import(this.dataSource.id);
  }
}
