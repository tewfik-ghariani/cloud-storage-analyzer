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
        $scope.exception = false;



        var customer = $state.params.customer;
        var object = $state.params.object;
        var headers = $state.params.headers;
        var conditions = $state.params.conditions;
        console.log(object);

        detailsFactory.query(customer, object, headers, conditions).then(function (response) {
            if (response.data.success) {
                data = response.data.data;
                $scope.content = data.content;
                $scope.selected_items = data.selected_items;
                $scope.progressbar.complete();
            }
            else {
                $scope.error = response.data.error;
                $scope.exception = true;
            }
        });

          for (head in $scope.selected_items) {
              $scope.columnDefs.push({headersName: head, field: head});
          }


    var columnDefs = [
        {headerName: "Make", field: "make"},
        {headerName: "Model", field: "model"},
        {headerName: "Price", field: "price"}
    ];


             var rowData = [
        {make: "Toyota", model: "Celica", price: 35000},
        {make: "Ford", model: "Mondeo", price: 32000},
        {make: "Porsche", model: "Boxter", price: 72000}
    ];


            $scope.gridOptions = {
        columnDefs: columnDefs,
        rowData: rowData,

    };

    }]);