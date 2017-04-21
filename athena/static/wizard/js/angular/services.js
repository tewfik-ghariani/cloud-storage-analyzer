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

        create_db: function (db) {
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
    }
}]);





app.factory('externalWizardFactory', ['$http', function ($http) {

    return {
        actionFile: function (file, type) {
            return $http({
                method: 'POST',
                url: '/wizard/external',
                data: {'fetch': type,
                        'file': file}
            })
        },

    }

}]);