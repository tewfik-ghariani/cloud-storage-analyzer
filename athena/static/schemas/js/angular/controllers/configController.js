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

        $scope.arrived = false;
        $scope.conds = [];
        $scope.progressbar.start();

        configFactory.getConfig(customer, object).then(function (response) {
            $scope.progressbar.complete();

            if (response.data.success) {
                data = response.data.data;
                $scope.headers = data.headers;
                $scope.user = {headers: []};
                $scope.object = data.object;
                $scope.customer = data.customer;
                $scope.bucket = data.bucket;
                $scope.nbr_headers = data.nbr_headers;
                $scope.xtraHeaders = [];
                $scope.arrived = true;
            }
            else {
                Flash.create('danger', response.data.error);
            }
        });


        $scope.query = function () {
            $('.modal').modal('hide');
            $('.modal-backdrop').remove();
            $('#body').removeClass('modal-open');

            var customer = $scope.customer;
            var object = $scope.object;
            var headers = $scope.user.headers;
            var xtraHeaders = $scope.xtraHeaders;
            var conditions = $scope.conds;
            var xtra = $scope.xtra;


            $state.go('details', params = {
                'customer': customer,
                'object': object,
                'headers': headers,
                'conditions': conditions,
                'xtra': xtra,
                'xtraHeaders': xtraHeaders
            });
        };

        $scope.checkAll = function () {
            $scope.user.headers = $scope.headers.map(function (item) {
                return item.attr;
            });
        };


        $scope.uncheckAll = function () {
            $scope.user.headers = [];
        };


        $scope.addCondition = function () {
            $scope.conds.push({'logical': 'AND', 'selected_column': '', 'operator': '', 'input': ''});
        };

        $scope.deleteCondition = function (id) {
            $scope.conds.splice(id, 1);
        };

        $scope.getOptions = function (html_type) {
            if (html_type == 'number') {
                options = ['=', '>', '<', '>=', '<=']
            }
            else {
                options = ['=', '!=', 'LIKE', 'NOT LIKE']
            }
            return options
        };


        $scope.custom_query = function () {

            var customer = $scope.customer;
            var object = $scope.object;
            var headers = $scope.custom_query_cols;
            var conditions = $scope.custom_query_conds;


            $state.go('details', params = {
                'customer': customer,
                'object': object,
                'headers': headers,
                'conditions': conditions,
                'custom': true
            });
        };


        $scope.FDVcheck = function () {
            $('.modal').modal('hide');
            $('.modal-backdrop').remove();
            $('#body').removeClass('modal-open');

            var customer = $scope.customer;
            var object = $scope.object;

            $state.go('FDV', params = {
                'customer': customer,
                'object': object
            });
        };

        $scope.addXtraHead = function () {
            $scope.xtraHeaders.push({'op': '', 'col': ''})
        };

        $scope.delXtraHead = function (id) {
            $scope.xtraHeaders.splice(id, 1);
        };
    }]);
