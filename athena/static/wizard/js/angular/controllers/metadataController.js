var app = angular.module('wizardApp');


app.controller('metadataController', [
    '$scope',
    'metadataWizardFactory',
    'Flash',
    function ($scope,
              metadataWizardFactory,
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
        $scope.FDVfields = [];
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

        metadataWizardFactory.getCustomers().then(function (response) {
            $scope.progressbar.complete();

            if (response.data.success) {
                data = response.data.data;
                $scope.customers = data.customers;
            }
            else {
                Flash.create('danger', reponse.data.error, 4000);
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
                'type': $scope.config_type || ''
            });
            customer = $scope.selected_customer;
            name = $scope.config_name;
            rows = $scope.configuration;

            $scope.progressbar.start();

            metadataWizardFactory.addConfig(customer, name, rows).then(function (response) {
                $scope.progressbar.complete();
                $scope.initForm();

                if (response.data.success) {
                    msg = response.data.msg;
                    Flash.create('success', msg, 4000);
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


        $scope.get_local_config = function () {
            $scope.showGrid = false;
            customer = $scope.fetched_customer;

            $scope.progressbar.start();

            metadataWizardFactory.get_local_config(customer).then(function (response) {
                $scope.progressbar.complete();

                if (response.data.success) {
                    $scope.showGrid = true;
                    $scope.rowData = response.data.rowData;
                    $scope.gridOptions.api.setRowData($scope.rowData);
                    $scope.gridOptions.api.refreshView();
                    $scope.gridOptions.api.sizeColumnsToFit();
                }
                else {
                    $scope.rowData = [];
                    Flash.create('danger', response.data.error, 5000);
                }
            });

        };

        $scope.select_object = function (element, id) {
            $scope.selected_object = {
                'label': element.currentTarget.innerText,
                'id': id
            };
            var customer = $scope.fetched_customer;
            var object = $scope.selected_object.label;

            $scope.progressbar.start();

            metadataWizardFactory.fetchFDV(customer, object).then(function (response) {
                $scope.progressbar.complete();

                if (response.data.success) {
                    data = response.data.data;
                    $scope.fieldsFDV = data.fieldsFDV;
                    $scope.temp_headers = data.headers;
                }
                else {
                    $(".modal").modal("hide");
                    Flash.create('danger', response.data.error, 5000);
                }
            });
        };


        $scope.addFDVRow = function () {
            $scope.fieldsFDV.push({'value': '', 'keys': [{'name': ''}]});
        };

        $scope.deleteFDVRow = function (id) {
            $scope.fieldsFDV.splice(id, 1);
        };

        $scope.saveFDV = function () {
            var customer = $scope.fetched_customer;
            var object = $scope.selected_object.label;
            var fieldsFDV = $scope.fieldsFDV;

            $scope.progressbar.start();

            metadataWizardFactory.updateFDV(customer, object, fieldsFDV).then(function (response) {
                $(".modal").modal("hide");
                $scope.progressbar.complete();

                if (response.data.success) {
                    $scope.fieldsFDV = [];
                    data = response.data.data;
                    Flash.create('success', data.msg, 4000);
                }
                else {
                    Flash.create('danger', response.data.error, 5000);
                }
            });
        };


        $scope.deleteConfig = function () {
            var customer = $scope.fetched_customer;
            var object = $scope.selected_object.label;
            var id = $scope.selected_object.id;

            $scope.progressbar.start();

            metadataWizardFactory.deleteConfig(customer, object).then(function (response) {
                $(".modal").modal("hide");
                $scope.progressbar.complete();

                if (response.data.success) {
                    $scope.rowData.splice(id, 1);
                    $scope.gridOptions.api.setRowData($scope.rowData);
                    $scope.gridOptions.api.refreshView();
                    msg = response.data.msg;
                    Flash.create('success', msg, 4000);
                }
                else {
                    Flash.create('danger', response.data.error, 5000);
                }
            });
        };

        $scope.delHeader = function (parent_id, id) {
            $scope.fieldsFDV[parent_id].keys.splice(id, 1);
        };

        $scope.addHeader = function (parent_id) {
            $scope.fieldsFDV[parent_id].keys.push({'name': ''});
        };

    }]);