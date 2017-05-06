var app = angular.module('schemaApp');


app.controller('detailsController', [
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
        $scope.search = '';

        $scope.gridOptions = {
            columnDefs: [],
            rowData: [],
            enableFilter: true,
            enableColResize: true,
            enableSorting: true,
        };

        var customer = $state.params.customer;
        var object = $state.params.object;
        var headers = $state.params.headers;
        var conditions = $state.params.conditions;
        var custom = $state.params.custom;


        detailsFactory.query(customer, object, headers, conditions, custom).then(function (response) {
            $scope.progressbar.complete();

            if (response.data.success) {
                data = response.data.data;
                $scope.content = data.content;
                $scope.headers = data.headers;
                $scope.arrived = true;
                Flash.create('danger', data.msg, false);

                $scope.columnDefs = [];
                for (head in $scope.headers) {
                    $scope.columnDefs.push({
                        headerName: $scope.headers[head],
                        field: $scope.headers[head]
                    });
                }


                $scope.rowData = [];
                for (row in $scope.content) {
                    new_line = {};
                    i = 0;
                    for (head in $scope.headers) {
                        new_line[$scope.headers[head]] = $scope.content[row][i];
                        i++;
                    }
                    $scope.rowData.push(new_line);
                }


                $scope.gridOptions.api.setColumnDefs($scope.columnDefs);
                $scope.gridOptions.api.refreshHeader();
                $scope.gridOptions.api.setRowData($scope.rowData);
                $scope.gridOptions.api.refreshView();
                $scope.gridOptions.api.sizeColumnsToFit();

            }
            else {
                $scope.gotError = true;
                Flash.create('danger', response.data.error, false);
            }
        });


        $scope.export = function () {
            $scope.gridOptions.api.exportDataAsCsv();
        };

        $scope.search_now = function () {
            $scope.gridOptions.api.setQuickFilter($scope.search);
        };

    }]);