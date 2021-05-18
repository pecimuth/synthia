import { ColumnView } from '../api/models';
import { DataSourceView } from '../api/models/data-source-view';
import { OutputFileDriverListView } from '../api/models/output-file-driver-list-view';
import { PreviewView } from '../api/models/preview-view';
import { ProjectListView } from '../api/models/project-list-view';
import { ProjectView } from '../api/models/project-view';
import { UserView } from '../api/models/user-view';

/**
 * Create mock objects for testing purposes.
 */
export namespace Mock {
  export function user(): UserView {
    return {
      email: 'mock@example.com',
      id: 42
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

  export function dataSourceDatabase(): DataSourceView {
    return {
      db: 'foobar', 
      driver: 'postgresql', 
      file_name: null, 
      host: 'examplehost', 
      id: 983, 
      mime_type: null, 
      port: 4321, 
      usr: 'baz'
    };
  }

  export function column(): ColumnView {
    return {
      col_type: 'string', 
      generator_setting: {
        id: 103, 
        name: 'FirstName', 
        null_frequency: 0.0, 
        params: {}
      }, 
      id: 126, 
      name: 'first_name', 
      nullable: false,
      reflected_column_idf: 'author.first_name'
    };
  }

  export function project(): ProjectView {
    return {
      'data_sources': [
        {
          'db': '/app/instance/project/3/zjRuWqFRYd_books.db', 
          'driver': 'sqlite', 
          'file_name': 'books.db', 
          'host': null, 
          'id': 6, 
          'mime_type': 'application/vnd.sqlite3', 
          'port': null, 
          'usr': null
        }, 
        {
          'db': 'db', 
          'driver': 'postgresql', 
          'file_name': null, 
          'host': 'localhost', 
          'id': 7, 
          'mime_type': null, 
          'port': 5432, 
          'usr': 'user'
        }, 
        {
          'db': null, 
          'driver': null, 
          'file_name': 'source.csv', 
          'host': null, 
          'id': 8, 
          'mime_type': 'text/csv', 
          'port': null, 
          'usr': null
        }
      ], 
      'id': 3, 
      'name': 'My Project 1', 
      'tables': [
        {
          'columns': [
            {
              'col_type': 'string', 
              'generator_setting': {
                'id': 103, 
                'name': 'FirstName', 
                'null_frequency': 0.0, 
                'params': {}
              }, 
              'id': 126, 
              'name': 'first_name', 
              'nullable': false
            }, 
            {
              'col_type': 'string', 
              'generator_setting': {
                'id': 104, 
                'name': 'LastName', 
                'null_frequency': 0.0, 
                'params': {}
              }, 
              'id': 147, 
              'name': 'last_name', 
              'nullable': false
            }, 
            {
              'col_type': 'datetime', 
              'generator_setting': {
                'id': 105, 
                'name': 'DateTime', 
                'null_frequency': 0.1, 
                'params': {
                  'end': '2021-01-01T00:00:00.000000Z', 
                  'start': '1970-01-01T00:00:00.000000Z'
                }
              }, 
              'id': 148, 
              'name': 'date_of_birth', 
              'nullable': true
            }, 
            {
              'col_type': 'string', 
              'generator_setting': {
                'id': 106, 
                'name': 'ForeignKey', 
                'null_frequency': 0.1, 
                'params': {}
              }, 
              'id': 149, 
              'name': 'home_country', 
              'nullable': true
            }, 
            {
              'col_type': 'string', 
              'generator_setting': {
                'id': 106, 
                'name': 'ForeignKey', 
                'null_frequency': 0.1, 
                'params': {}
              }, 
              'id': 150, 
              'name': 'home_city', 
              'nullable': true
            }
          ], 
          'constraints': [
            {
              'check_expression': null, 
              'constrained_columns': [
                {
                  'id': 126, 
                  'name': 'first_name'
                }, 
                {
                  'id': 147, 
                  'name': 'last_name'
                }
              ], 
              'constraint_type': 'primary', 
              'id': 81, 
              'name': 'pk_author', 
              'referenced_columns': []
            }, 
            {
              'check_expression': null, 
              'constrained_columns': [
                {
                  'id': 149, 
                  'name': 'home_country'
                }, 
                {
                  'id': 150, 
                  'name': 'home_city'
                }
              ], 
              'constraint_type': 'foreign', 
              'id': 93, 
              'name': 'fk_author_place', 
              'referenced_columns': [
                {
                  'id': 136, 
                  'name': 'country', 
                  'table': {
                    'id': 30, 
                    'name': 'place'
                  }
                }, 
                {
                  'id': 137, 
                  'name': 'city', 
                  'table': {
                    'id': 30, 
                    'name': 'place'
                  }
                }
              ]
            }
          ], 
          'generator_settings': [
            {
              'id': 103, 
              'name': 'FirstName', 
              'null_frequency': 0.0, 
              'params': {}
            }, 
            {
              'id': 104, 
              'name': 'LastName', 
              'null_frequency': 0.0, 
              'params': {}
            }, 
            {
              'id': 105, 
              'name': 'DateTime', 
              'null_frequency': 0.1, 
              'params': {
                'end': '2021-01-01T00:00:00.000000Z', 
                'start': '1970-01-01T00:00:00.000000Z'
              }
            }, 
            {
              'id': 106, 
              'name': 'ForeignKey', 
              'null_frequency': 0.1, 
              'params': {}
            }
          ], 
          'id': 26, 
          'name': 'author'
        }, 
        {
          'columns': [
            {
              'col_type': 'string', 
              'generator_setting': {
                'id': 116, 
                'name': 'Word', 
                'null_frequency': 0.0, 
                'params': {}
              }, 
              'id': 128, 
              'name': 'company_name', 
              'nullable': false
            }, 
            {
              'col_type': 'string', 
              'generator_setting': {
                'id': 117, 
                'name': 'ForeignKey', 
                'null_frequency': 0.1, 
                'params': {}
              }, 
              'id': 129, 
              'name': 'parent_company', 
              'nullable': true
            }, 
            {
              'col_type': 'bool', 
              'generator_setting': {
                'id': 118, 
                'name': 'Bernoulli', 
                'null_frequency': 0.1, 
                'params': {
                  'success_probability': 0.5
                }
              }, 
              'id': 130, 
              'name': 'is_public_company', 
              'nullable': true
            }
          ], 
          'constraints': [
            {
              'check_expression': null, 
              'constrained_columns': [
                {
                  'id': 129, 
                  'name': 'parent_company'
                }
              ], 
              'constraint_type': 'foreign', 
              'id': 85, 
              'name': 'fk_publisher_parent', 
              'referenced_columns': [
                {
                  'id': 128, 
                  'name': 'company_name', 
                  'table': {
                    'id': 28, 
                    'name': 'publisher'
                  }
                }
              ]
            }, 
            {
              'check_expression': 'publisher.is_public_company IN (:param_1, :param_2)', 
              'constrained_columns': [
                {
                  'id': 130, 
                  'name': 'is_public_company'
                }
              ], 
              'constraint_type': 'check', 
              'id': 86, 
              'name': '_unnamed_', 
              'referenced_columns': []
            }, 
            {
              'check_expression': null, 
              'constrained_columns': [
                {
                  'id': 128, 
                  'name': 'company_name'
                }
              ], 
              'constraint_type': 'primary', 
              'id': 87, 
              'name': 'pk_publisher', 
              'referenced_columns': []
            }, 
            {
              'check_expression': 'is_public_company IN (0, 1)', 
              'constrained_columns': [], 
              'constraint_type': 'check', 
              'id': 88, 
              'name': null, 
              'referenced_columns': []
            }
          ], 
          'generator_settings': [
            {
              'id': 116, 
              'name': 'Word', 
              'null_frequency': 0.0, 
              'params': {}
            }, 
            {
              'id': 117, 
              'name': 'ForeignKey', 
              'null_frequency': 0.1, 
              'params': {}
            }, 
            {
              'id': 118, 
              'name': 'Bernoulli', 
              'null_frequency': 0.1, 
              'params': {
                'success_probability': 0.5
              }
            }
          ], 
          'id': 28, 
          'name': 'publisher'
        }, 
        {
          'columns': [
            {
              'col_type': 'string', 
              'generator_setting': {
                'id': 107, 
                'name': 'Country', 
                'null_frequency': 0.0, 
                'params': {}
              }, 
              'id': 136, 
              'name': 'country', 
              'nullable': false
            }, 
            {
              'col_type': 'string', 
              'generator_setting': {
                'id': 108, 
                'name': 'City', 
                'null_frequency': 0.0, 
                'params': {}
              }, 
              'id': 137, 
              'name': 'city', 
              'nullable': false
            }
          ], 
          'constraints': [
            {
              'check_expression': null, 
              'constrained_columns': [
                {
                  'id': 136, 
                  'name': 'country'
                }, 
                {
                  'id': 137, 
                  'name': 'city'
                }
              ], 
              'constraint_type': 'primary', 
              'id': 92, 
              'name': 'pk_place', 
              'referenced_columns': []
            }
          ], 
          'generator_settings': [
            {
              'id': 107, 
              'name': 'Country', 
              'null_frequency': 0.0, 
              'params': {}
            }, 
            {
              'id': 108, 
              'name': 'City', 
              'null_frequency': 0.0, 
              'params': {}
            }
          ], 
          'id': 30, 
          'name': 'place'
        }
      ]
    };    
  }

  export function preview(): PreviewView {
    return {
      'tables': {
        'author': [
          {
            'date_of_birth': '2007-05-25 09:14:25', 
            'first_name': 'Jessica', 
            'home_city': 'Allenton', 
            'home_country': 'Ghana', 
            'last_name': 'Medina'
          }, 
          {
            'date_of_birth': '2007-12-31 04:43:12', 
            'first_name': 'David', 
            'home_city': 'Hayesmouth', 
            'home_country': 'British Virgin Islands', 
            'last_name': 'Thomas'
          }, 
          {
            'date_of_birth': '1979-03-22 00:09:44', 
            'first_name': 'Robert', 
            'home_city': 'Hayesmouth', 
            'home_country': 'British Virgin Islands', 
            'last_name': 'Ross'
          }, 
          {
            'date_of_birth': '2013-03-07 23:34:40', 
            'first_name': 'Michael', 
            'home_city': 'Hayesmouth', 
            'home_country': 'British Virgin Islands', 
            'last_name': 'Morgan'
          }, 
          {
            'date_of_birth': '1975-08-08 12:43:09', 
            'first_name': 'Scott', 
            'home_city': 'Allenton', 
            'home_country': 'Ghana', 
            'last_name': 'Brown'
          }
        ], 
        'place': [
          {
            'city': 'North Elizabethberg', 
            'country': 'Guinea-Bissau'
          }, 
          {
            'city': 'Rachaelborough', 
            'country': 'Suriname'
          }, 
          {
            'city': 'Maysview', 
            'country': 'Northern Mariana Islands'
          }, 
          {
            'city': 'Hayesmouth', 
            'country': 'British Virgin Islands'
          }, 
          {
            'city': 'Allenton', 
            'country': 'Ghana'
          }
        ], 
        'publisher': [
          {
            'company_name': 'west', 
            'is_public_company': false, 
            'parent_company': null
          }, 
          {
            'company_name': 'pay', 
            'is_public_company': true, 
            'parent_company': 'west'
          }, 
          {
            'company_name': 'company', 
            'is_public_company': false, 
            'parent_company': 'west'
          }, 
          {
            'company_name': 'bit', 
            'is_public_company': false, 
            'parent_company': 'west'
          }, 
          {
            'company_name': 'sister', 
            'is_public_company': false, 
            'parent_company': 'bit'
          }
        ]
      }
    }    
  }
}
