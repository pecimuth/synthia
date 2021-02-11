import { Component, Input, OnInit } from '@angular/core';
import { DataSourceView } from 'src/app/api/models/data-source-view';
import { ResourceService } from 'src/app/project/service/resource.service';

@Component({
  selector: 'app-resource',
  templateUrl: './resource.component.html',
  styleUrls: ['./resource.component.scss']
})
export class ResourceComponent implements OnInit {

  @Input() data_source: DataSourceView;
  
  constructor(public resourceService: ResourceService) { }

  ngOnInit(): void {
  }
}
