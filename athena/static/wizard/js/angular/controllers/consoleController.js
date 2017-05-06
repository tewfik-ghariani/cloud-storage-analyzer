var app = angular.module('wizardApp');


app.controller('consoleController', [
    '$scope',
    'consoleWizardFactory',
    'Flash',
    function ($scope,
              consoleWizardFactory,
              Flash) {

        $scope.init_table = function () {
            $scope.columns = [];
            $scope.col_attr = '';
            $scope.col_type = '';
            $scope.selected_db = '';
            $scope.table_name = '';
            $scope.delim = '';
        };

        $scope.columns = [];
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

        var done = "<b> Success!</b>";


        $scope.dbs = function () {
            var info_id = Flash.create('info', "<b> Retrieving Databases.. </b>", 0, false);
            $scope.tables = [];
            $scope.no_tables = null;
            $scope.parent_db = null;
            $scope.progressbar.start();

            consoleWizardFactory.queryDBS().then(function (response) {
                data = response.data;
                $scope.progressbar.complete();
                Flash.dismiss(info_id);

                if (data.success) {
                    $scope.databases = data.data;
                    Flash.create('success', done, 2000);
                }
                else {
                    Flash.create('danger', response.data.error, false);
                }
            });
        };


        $scope.get_tables = function () {
            $scope.parent_db = null;
            $scope.no_tables = null;
            $scope.tables = [];
            database = this.db;
            var id = Flash.create('info', "<b> Retrieving tables from </b>" + database + '..', 0, false);
            $scope.progressbar.start();

            consoleWizardFactory.queryTables(database).then(function (response) {
                data = response.data;
                Flash.dismiss(id);
                $scope.progressbar.complete();

                if (data.success) {
                    $scope.parent_db = data.db;
                    if (data.data == 'None') {
                        $scope.no_tables = 'No Tables found in';
                        $scope.tables = [];
                    }
                    else {
                        $scope.no_tables = 'Tables in ';
                        $scope.tables = data.data;
                    }
                    Flash.create('success', done, 2000);
                }
                else {
                    Flash.create('danger', response.data.error, false);
                }
            });
        };

        $scope.associate = function () {
            $scope.to_delete = this.db || this.table;
            if (this.db) {
                $scope.type = 'database'
            }
            else {
                $scope.type = 'table'
            }
        };

        $scope.delete = function () {
            type = $scope.type;
            to_delete = $scope.to_delete;
            parent_db = $scope.parent_db;
            var id = Flash.create('danger', "<b> Deleting : </b>" + type + ' ' + to_delete + '..', 0, false);
            $scope.progressbar.start();
            $(".modal").modal("hide");

            consoleWizardFactory.delete(to_delete, type, parent_db).then(function (response) {
                Flash.dismiss(id);
                $scope.progressbar.complete();

                if (response.data.success) {
                    Flash.create('success', type + ' ' + to_delete + ' deleted!', 2000);
                }
                else {
                    Flash.create('danger', response.data.error, false);
                }
            });
        };


        $scope.new_db = function () {
            $(".modal").modal("hide");
            database = $scope.new_database;
            var id = Flash.create('info', "<b> Creating database : </b>" + database + '..', 0, false);
            $scope.progressbar.start();

            consoleWizardFactory.createDB(database).then(function (response) {
                Flash.dismiss(id);
                $scope.progressbar.complete();

                if (response.data.success) {
                    Flash.create('success', database + ' created!', 2000);
                }
                else {
                    Flash.create('danger', response.data.error, false);
                }
            });
        };


        $scope.createTable = function () {
            $(".modal").modal("hide");

            // toAdd the first column
            $scope.columns.unshift({'attr': $scope.col_attr, 'type': $scope.col_type});
            columns = $scope.columns;
            delim = $scope.delim;
            database = $scope.selected_db;
            table = $scope.table_name;

            var id = Flash.create('info', "<b> Creating Table : </b>" + table + '..', 0, false);
            $scope.progressbar.start();

            consoleWizardFactory.createTable(columns,
                delim,
                database,
                table).then(function (response) {
                Flash.dismiss(id);
                $scope.progressbar.complete();
                $scope.init_table();

                if (response.data.success) {
                    Flash.create('success', table + ' created!', 2000);
                }
                else {
                    Flash.create('danger', response.data.error, false);
                }
            });

        };

        $scope.addColumn = function () {
            $scope.columns.push({'attr': '', 'type': ''})
        };

        $scope.deleteColumn = function (id) {
            $scope.columns.splice(id, 1);
        };
    }]);
