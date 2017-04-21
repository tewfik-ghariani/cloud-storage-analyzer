var app = angular.module('schemaApp');


app.controller('configController', [
    '$scope',
    'Flash',
    'configFactory',
    '$state',
    function ($scope,
              Flash,
              configFactory,
              $state) {

        var customer = $state.params.customer;
        var object = $state.params.object;

        $scope.progressbar.start();
        $scope.conds = [];

        configFactory.getConfig(customer, object).then(function (response) {
            if (response.data.success) {
                data = response.data.data;
                $scope.headers = data.headers;
                $scope.user = {headers: []};
                $scope.object = data.object;
                $scope.customer = data.customer;
                $scope.bucket = data.bucket;
                $scope.progressbar.complete();
            }
            else {
                alert('Configuration not Set yet!');
            }
        });


        $scope.query = function () {
            var customer = $scope.customer;
            var object = $scope.object;
            var headers = $scope.user.headers;
            var conditions = $scope.conds;


            $state.go('details', params = {
                'customer': customer,
                'object': object,
                'headers': headers,
                'conditions': conditions
            });
        };

        $scope.checkAll = function () {
            $scope.user.headers = $scope.headers.map(function (item) {
                return item.attribute;
            });
        };


        $scope.uncheckAll = function () {
            $scope.user.headers = [];
        };


        $scope.addCondition = function () {
            $scope.conds.push({'selected_column': '', 'operator': '', 'input': ''});
        };

        $scope.deleteCondition = function (id) {
            $scope.conds.splice(id, 1);
        };

        $scope.getOptions = function (html_type) {
            if (html_type == 'number') {
                options = ['=', '>', '<', '>=', '<=']
            }
            else {
                options = ['=', 'LIKE', 'NOT LIKE']
            }
            return options

        };
    }]);