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

    }

}]);


app.factory('databaseWizardFactory', ['$http', function ($http) {

    return {
        getCustomers: function () {
            return $http({
                method: 'POST',
                url: '/wizard/database',
                data: {
                    'fetch': 'customers',
                }
            })
        },

        addConfig: function (customer, name, rows) {
            return $http({
                method: 'POST',
                url: '/wizard/database',
                data: {
                    'fetch': 'addConfig',
                    'customer': customer,
                    'name': name,
                    'rows': rows
                }
            })
        },

        getConfig: function(customer) {
            return $http({
                method: 'POST',
                url: '/wizard/database',
                data: {
                    'fetch': 'getConfig',
                    'customer': customer
                }
            })
        },
    }

}]);