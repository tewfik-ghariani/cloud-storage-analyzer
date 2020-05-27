var app = angular.module('schemaApp');


app.factory('listFactory', ['$http', function ($http) {

    return {
        getList: function (customer_shortcut, prefix=null, back=false) {
            return $http({
                method: 'POST',
                url: '/list/',
                data: {
                    'fetch': 'objects',
                    'customer': customer_shortcut,
                    'prefix': prefix,
                    'back': back
                }
            })

        },

        download: function (customer, object) {
            return $http({
                method: 'POST',
                url: '/list/',
                data: {
                    'fetch': 'download',
                    'customer': customer,
                    'object': object
                }
            })
        },

        search: function (regex, customer) {
            return $http({
                method: 'POST',
                url: '/list/',
                data: {
                    'fetch': 'search',
                    'regex': regex,
                    'customer': customer
                }
            })
        },

        getSize: function (customer, object) {
            return $http({
                method: 'POST',
                url: '/list/',
                data: {
                    'fetch': 'size',
                    'customer': customer,
                    'object': object
                }
            })
        }
    }
}]);


app.factory('configFactory', ['$http', function ($http) {

    return {
        getConfig: function (customer, object) {
            return $http({
                method: 'POST',
                url: '/config/',
                data: {
                    'fetch': 'configuration',
                    'customer': customer,
                    'object': object
                }
            })
        }
    }
}]);


app.factory('detailsFactory', ['$http', function ($http) {

    return {

        query: function (customer, object, headers, conditions, custom=false, xtra=false, xtraHeaders) {
            return $http({
                method: 'POST',
                url: '/details/',
                data: {
                    'fetch': 'details',
                    'customer': customer,
                    'object': object,
                    'headers': headers,
                    'conditions': conditions,
                    'custom': custom,
                    'xtra': xtra,
                    'xtraHeaders': xtraHeaders
                }
            })
        },

        more: function (query_id, startRow, endRow) {
            return $http({
                method: 'POST',
                url: '/details/',
                data: {
                    'fetch': 'more',
                    'query_id': query_id,
                    'startRow': startRow,
                    'endRow': endRow
                }
            })
        },

        export: function (query_id) {
            return $http({
                method: 'POST',
                url: '/details/',
                data: {
                    'fetch': 'export',
                    'query_id': query_id
                }
            })
        },

        FDVcheck: function (customer, object) {
            return $http({
                method: 'POST',
                url: '/FDV/',
                data: {
                    'fetch': 'FDVcheck',
                    'customer': customer,
                    'object': object
                }
            })
        }
    }

}]);
