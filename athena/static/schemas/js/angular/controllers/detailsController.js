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
            enableFilter: true,
            enableColResize: true,
            enableSorting: true,
            rowModelType: 'infinite',
            maxPagesInCache: 2,
            //   pagination: true,
            // paginationAutoPageSize: true
        };

        var ID = {
            headerName: "ID", width: 50,
            cellRenderer: function (params) {
                if (params.data !== undefined) {
                    return params.node.id;
                } else {
                    return '<div class="loader"></div>'
                }
            }
        };


        function setRowData() {
            var dataSource = {
                rowCount: null,
                getRows: function (params) {
                    var query_id = $scope.query_id;
                    $scope.progressbar.start();
                    detailsFactory.more(query_id, params.startRow, params.endRow).then(function (response) {
                        $scope.progressbar.complete();
                        rowsThisPage = response.data.data.rowData;
                        lastRow = response.data.data.lastRow;
                        params.successCallback(rowsThisPage, lastRow);
                    })
                }
            };
            $scope.gridOptions.api.setDatasource(dataSource);
        }


        var customer = $state.params.customer;
        var object = $state.params.object;
        var headers = $state.params.headers;
        var conditions = $state.params.conditions;
        var custom = $state.params.custom;
        var xtra = $state.params.xtra;
        var xtraHeaders = $state.params.xtraHeaders;


        detailsFactory.query(customer,
            object,
            headers,
            conditions,
            custom,
            xtra,
            xtraHeaders).then(function (response) {
            $scope.progressbar.complete();

            if (response.data.success) {
                data = response.data.data;
                data.columnDefs.unshift(ID);
                $scope.arrived = true;
                Flash.create('danger', data.msg, false);
                $scope.query_id = data.query_id;
                setRowData();

                $scope.gridOptions.api.setColumnDefs(data.columnDefs);
                $scope.gridOptions.api.refreshHeader();
                $scope.gridOptions.api.refreshView();
                $scope.gridOptions.api.sizeColumnsToFit();

            }
            else {
                $scope.gotError = true;
                // default fruit fly bug:
                new BugController({});

                // default spiders:
                new SpiderController({});

                Flash.create('danger', response.data.error, false);
            }
        });


        $scope.export = function () {
            var query_id = $scope.query_id;
            var flash_msg = " Exporting results..";
            var info_id = Flash.create('info', flash_msg, 0, false);
            $scope.progressbar.start();

            detailsFactory.export(query_id).then(function (response) {
                $scope.progressbar.complete();
                Flash.dismiss(info_id);

                if (response.status == 200) {
                    var anchor = angular.element('<a/>');
                    anchor.css({display: 'none'}); // Make sure it's not visible
                    angular.element(document.body).append(anchor); // Attach to document

                    anchor.attr({
                        href: 'data:attachment/csv;charset=utf-8,' + encodeURI(response.data),
                        target: '_blank',
                        download: 'Results.csv'
                    })[0].click();

                    anchor.remove(); // Clean it up afterwards
                }
                else {
                    Flash.create('danger', 'Could not export');
                }
            })
        };

        $scope.search_now = function () {
            $scope.gridOptions.api.setQuickFilter($scope.search);
        };

    }]);
