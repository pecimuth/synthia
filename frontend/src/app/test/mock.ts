import { OutputFileDriverListView } from '../api/models/output-file-driver-list-view';
import { ProjectView } from '../api/models/project-view';

export namespace Mock {
  export function project(): ProjectView {
    return {
      tables: [
        {name: 'Foo'},
        {name: 'Bar'},
        {name: 'Baz'}
      ]
    };
  }

  export function outputFileDrivers(): OutputFileDriverListView {
    return {
      items: [
        {driver_name: 'foo', display_name: 'Foo', mime_type: 'application/foo'},
        {driver_name: 'bar', display_name: 'Bar', mime_type: 'application/bar'}
      ]
    };
  }
}
