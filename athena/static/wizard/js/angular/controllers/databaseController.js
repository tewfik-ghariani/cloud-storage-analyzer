var app = angular.module('wizardApp');


app.controller('databaseController', [
    '$scope',
    'databaseWizardFactory',
    'Flash',
    function ($scope,
              databaseWizardFactory,
              Flash) {


        function getNodeChildDetails(rowItem) {
            if (rowItem.group) {
                return {
                    group: true,
                    children: rowItem.participants,
                    field: 'group',
                    key: rowItem.group
                };
            } else {
                return null;
            }
        }

        $scope.showGrid = false;
        $scope.configuration = [];
        $scope.common_types = [
            'string',
            'tinyint',
            'smallint',
            'int',
            'bigint',
            'boolean',
            'float',
            'double',
            'array',
            'map',
            'timestamp'
        ];

        $scope.columnDefs = [
            {
                headerName: 'Name',
                cellRenderer: 'group',
                editable: function (params) {
                    return !params.node.group;
                }
            },
            {
                headerName: "Fields",
                children: [
                    {headerName: "Attribute", field: "attr", editable: true},
                    {
                        headerName: "Html Type",
                        field: "html_type",
                        editable: true
                    },
                    {
                        headerName: "Type",
                        field: "type",
                        editable: true,
                        cellEditor: 'select',
                        cellEditorParams: {
                            values: $scope.common_types
                        }
                    }
                ]
            }
        ];

        $scope.gridOptions = {
            columnDefs: $scope.columnDefs,
            rowData: [],
            enableFilter: true,
            enableColResize: true,
            enableGroupEdit: true,
            enableSorting: true,
            getNodeChildDetails: getNodeChildDetails,
        };

        $scope.progressbar.start();

        databaseWizardFactory.getCustomers().then(function (response) {
            $scope.progressbar.complete();

            if (response.data.success) {
                data = response.data.data;
                $scope.customers = data.customers;
            }
            else {
                Flash.create('danger', reponse.data.error);
            }

        });

        $scope.addRow = function () {
            $scope.configuration.push({'attr': '', 'type': ''});
        };

        $scope.deleteRow = function (id) {
            $scope.configuration.splice(id, 1);
        };


        $scope.addConfig = function () {
            $(".modal").modal("hide");

            // toAdd the first row
            $scope.configuration.unshift({
                'attr': $scope.config_attr,
                'type': $scope.config_type
            });
            customer = $scope.selected_customer;
            name = $scope.config_name;
            rows = $scope.configuration;

            var id = Flash.create('info', "<b> Adding configuration : "
                + name
                + ' in '
                + customer.label
                + '..', 0, false);
            $scope.progressbar.start();


            databaseWizardFactory.addConfig(customer, name, rows).then(function (response) {
                $scope.progressbar.complete();
                $scope.initForm();
                Flash.dismiss(id);

                if (response.data.success) {
                    Flash.create('success', "<b>" + name + " configuration for "
                        + customer.label
                        + " added!", 4000);
                }
                else {
                    Flash.create('danger', response.data.error, 5000);
                }
            });
        };


        $scope.initForm = function () {
            $scope.config_attr = '';
            $scope.config_type = '';
            $scope.configuration = [];
            $scope.selected_customer = '';
            $scope.config_name = '';
        };


        $scope.getConfig = function () {
            $scope.showGrid = false;
            customer = $scope.fetched_customer;
            if (customer) {

                $scope.progressbar.start();

                databaseWizardFactory.getConfig(customer).then(function (response) {
                    $scope.progressbar.complete();

                    if (response.data.success) {
                        $scope.showGrid = true;
                        $scope.rowData = response.data.rowdata;
                        $scope.gridOptions.api.setRowData($scope.rowData);
                        $scope.gridOptions.api.refreshView();
                        $scope.gridOptions.api.sizeColumnsToFit();
                    }
                    else {
                        Flash.create('danger', response.data.error);
                    }
                });
            }
            else {
                Flash.create('danger', 'Choose a customer');
            }
        };

    }]);