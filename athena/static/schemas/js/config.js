var app = angular.module('schemaApp');

app.config([
    '$stateProvider',
    '$urlRouterProvider',
    function ($stateProvider,
              $urlRouterProvider) {

        $urlRouterProvider.otherwise('/index');

        $stateProvider

            .state('list', {
                url: '/list',
                params: {
                    customer_shortcut: null
                },
                templateUrl: 'list',
                controller: 'listController'
            })


            .state('config', {
                url: '/config',
                params: {
                    customer: null,
                    object: null
                },
                templateUrl: 'config',
                controller: 'configController'
            })


            .state('details', {
                url: '/details',
                params: {
                    customer: null,
                    object: null,
                    headers: null,
                    conditions: null
                },
                templateUrl: 'details',
                controller: 'detailsController'
            });


    }]);