var app = angular.module('schemaApp');


app.controller('FDVController', [
    '$scope',
    'Flash',
    'detailsFactory',
    '$state',
    function ($scope,
              Flash,
              detailsFactory,
              $state) {

        $scope.progressbar.start();
        $scope.arrived = false;
        $scope.gotError = false;

        var customer = $state.params.customer;
        var object = $state.params.object;

        detailsFactory.FDVcheck(customer, object).then(function (response) {
            $scope.progressbar.complete();

            if (response.data.success) {
                data = response.data.data;
                $scope.content = data.content;
                console.log(data.content);
                $scope.arrived = true;
                Flash.create('danger', data.msg, false);

            }
            else {
                $scope.gotError = true;
                Flash.create('danger', response.data.error, false);
            }
        });


    }]);