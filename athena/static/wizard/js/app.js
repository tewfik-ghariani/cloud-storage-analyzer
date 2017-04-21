var app = angular.module('wizardApp', [
    'ngProgress',
    'ngAnimate',
    'ngFlash',
]);


app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});


app.run(['$rootScope', 'ngProgressFactory', '$http', '$location',
    function ($rootScope, ngProgressFactory, $http, $location) {


        $rootScope.switchTo = function (headed) {
            return $location.url(headed);
        };


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