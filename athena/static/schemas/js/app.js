agGrid.initialiseAgGridWithAngular1(angular);

var app = angular.module('schemaApp', [
    'agGrid',
    'ui.router',
    'ngProgress',
    'ngAnimate',
    'ngFlash',
    'checklist-model',
]);


app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});


app.run(['$rootScope', 'ngProgressFactory', '$http',
    function ($rootScope, ngProgressFactory, $http) {

        $http.defaults.xsrfHeaderName = 'X-CSRFToken';
        $http.defaults.xsrfCookieName = 'csrftoken';


        $rootScope.progressbar = ngProgressFactory.createInstance();


        $rootScope.$on("$routeChangeStart", function () {
            $rootScope.progressbar.start();
        });


        $rootScope.$on("$routeChangeSuccess", function () {
            $rootScope.progressbar.complete();
        });

    }]);
