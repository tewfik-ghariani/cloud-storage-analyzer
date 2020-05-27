var app = angular.module('wizardApp');


app.factory('consoleWizardFactory', ['$http', function ($http) {

    return {
        queryDBS: function () {
            return $http({
                method: 'POST',
                url: '/wizard/console',
                data: {'fetch': 'dbs'}
            })

        },


        queryTables: function (db) {
            return $http({
                method: 'POST',
                url: '/wizard/console',
                data: {
                    'fetch': 'tables',
                    'database': db
                }
            })
        },


        delete: function (to_delete, type, parent_db) {
            if (type == 'database') {
                return $http({
                    method: 'POST',
                    url: '/wizard/console',
                    data: {
                        'fetch': 'manip_db',
                        'manip': 'delete_db',
                        'database': to_delete
                    }
                })
            }
            else {
                return $http({
                    method: 'POST',
                    url: '/wizard/console',
                    data: {
                        'fetch': 'delete_table',
                        'table': to_delete,
                        'parent_db': parent_db
                    }
                })
            }
        },

        createDB: function (db) {
            return $http({
                method: 'POST',
                url: '/wizard/console',
                data: {
                    'fetch': 'manip_db',
                    'manip': 'create_db',
                    'database': db
                }
            })
        },

        createTable: function (columns, delim, database, table) {
            return $http({
                method: 'POST',
                url: '/wizard/console',
                data: {
                    'fetch': 'create_table',
                    'columns': columns,
                    'delim': delim,
                    'database': database,
                    'table': table
                }
            })
        },

        desc_table: function (database, table) {
            return $http({
                method: 'POST',
                url: '/wizard/console',
                data: {
                    'fetch': 'desc_table',
                    'database': database,
                    'table': table
                }
            })
        }
    }
}]);


app.factory('externalWizardFactory', ['$http', function ($http) {

    return {
        actionFile: function (file, fetch) {
            return $http({
                method: 'POST',
                url: '/wizard/external',
                data: {
                    'fetch': fetch,
                    'file': file
                }
            })
        },

        getObjects: function (prefix=null, back=false) {
            return $http({
                method: 'POST',
                url: '/wizard/external',
                data: {
                    'fetch': 'objects',
                    'prefix': prefix,
                    'back': back
                }
            })
        },

        getSize: function (object) {
            return $http({
                method: 'POST',
                url: '/wizard/external',
                data: {
                    'fetch': 'size',
                    'object': object
                }
            })
        }

    }

}]);


app.factory('metadataWizardFactory', ['$http', function ($http) {

    return {
        getCustomers: function () {
            return $http({
                method: 'POST',
                url: '/wizard/metadata',
                data: {
                    'fetch': 'customers',
                }
            })
        },

        addConfig: function (customer, name, rows) {
            return $http({
                method: 'POST',
                url: '/wizard/metadata',
                data: {
                    'fetch': 'addConfig',
                    'customer': customer,
                    'name': name,
                    'rows': rows
                }
            })
        },

        get_local_config: function (customer) {
            return $http({
                method: 'POST',
                url: '/wizard/metadata',
                data: {
                    'fetch': 'get_local_config',
                    'customer': customer
                }
            })
        },

        fetchFDV: function (customer, object) {
            return $http({
                method: 'POST',
                url: '/wizard/metadata',
                data: {
                    'fetch': 'fetchFDV',
                    'customer': customer,
                    'object': object
                }
            })
        },

        updateFDV: function (customer, object, fieldsFDV) {
            return $http({
                method: 'POST',
                url: '/wizard/metadata',
                data: {
                    'fetch': 'updateFDV',
                    'customer': customer,
                    'object': object,
                    'fieldsFDV': fieldsFDV
                }
            })
        },

        deleteConfig: function (customer, object) {
            return $http({
                method: 'POST',
                url: '/wizard/metadata',
                data: {
                    'fetch': 'deleteConfig',
                    'customer': customer,
                    'object': object
                }
            })
        },
    }
}]);
