var app = angular.module('wizardApp');


app.controller('consoleController', [
    '$scope',
    'consoleWizardFactory',
    'Flash',
    function (
        $scope,
        consoleWizardFactory,
        Flash
    ) {


        var done = "<b> Success!</b>";

        $scope.dbs = function () {
            var info_id = Flash.create('info', "<b> Retrieving Databases.. </b>", 0, false);
            $scope.tables = [];
            $scope.no_tables = null;
            $scope.parent_db = null;
            $scope.progressbar.start();
            consoleWizardFactory.queryDBS().then(function (data) {
                data = data.data;
                if (data.success) {
                    $scope.progressbar.complete();
                    Flash.dismiss(info_id);

                    $scope.databases = data.data;
                    Flash.create('success', done, 2000);
                }
            });
        };


        $scope.get_tables = function () {
            $scope.parent_db = null;
            $scope.no_tables = null;
            $scope.tables = [];
            database = this.db;
            var id = Flash.create('info', "<b> Retrieving tables from </b>" + database + '..',0, false);
            $scope.progressbar.start();

            consoleWizardFactory.queryTables(database).then(function (data) {
                data = data.data;
                if (data.success) {
                    Flash.dismiss(id);
                    $scope.progressbar.complete();
                    $scope.parent_db = data.db;
                    if (data.data == 'None') {
                        $scope.no_tables = 'No Tables found in';
                        $scope.tables = [];
                    }
                    else {
                        $scope.no_tables = 'Tables in ';
                        $scope.tables = data.data; }
                    Flash.create('success', done, 2000);
                }
            });
        };

        $scope.associate = function () {
            $scope.to_delete = this.db || this.table;
            if (this.db) { $scope.type = 'database'}
            else { $scope.type = 'table' }
        };

        $scope.delete = function () {
            type = $scope.type;
            to_delete = $scope.to_delete;
            parent_db = $scope.parent_db;
            var id = Flash.create('danger', "<b> Deleting : </b>" + type + ' ' +  to_delete + '..',0, false);
            $scope.progressbar.start();
            $(".modal").modal("hide");
            consoleWizardFactory.delete(to_delete, type, parent_db).then(function (data) {
                if (data.data.success) {
                    Flash.dismiss(id);
                    $scope.progressbar.complete();
                    Flash.create('success', type + ' ' + to_delete + ' deleted!', 2000);

                }
            });
        };


        $scope.new_db = function () {
            database = $scope.new_database;
            var id = Flash.create('info', "<b> Creating database : </b>" + database + '..', 0, false);
            $scope.progressbar.start();
            consoleWizardFactory.create_db(database).then(function (data) {
                if (data.data.success) {
                    Flash.dismiss(id);
                    $scope.progressbar.complete();
                    Flash.create('success', database + ' created!', 2000);

                }
            });
        };

    }]);