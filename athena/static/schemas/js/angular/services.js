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

        query: function (customer, object, headers, conditions, custom=false) {
            return $http({
                method: 'POST',
                url: '/details/',
                data: {
                    'fetch': 'details',
                    'customer': customer,
                    'object': object,
                    'headers': headers,
                    'conditions': conditions,
                    'custom': custom
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