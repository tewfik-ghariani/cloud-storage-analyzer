var app = angular.module('wizardApp');


app.controller('externalController', [
    '$scope',
    'externalWizardFactory',
    'Flash',
    function ($scope,
              externalWizardFactory,
              Flash) {


        var done = "<b> Success!</b>";

        $scope.delete = function (element) {
            file = element.currentTarget.value;
            type = element.currentTarget.name;
            $scope.progressbar.start();

            var info_id = Flash.create('danger', "<b> Deleting file.. </b>" + file, 0, false);

            externalWizardFactory.actionFile(file, type).then(function (data) {
                data = data.data;
                if (data.success) {
                    $scope.progressbar.complete();
                    Flash.dismiss(info_id);
                    Flash.create('success', file + ' deleted!', 2000);
                }
            });
        };


        $scope.download = function (element) {
            file = element.currentTarget.value;
            type = element.currentTarget.name;
            $scope.progressbar.start();
            var info_id = Flash.create('info', "<b> Downloading file.. </b>" + file, 0, false);

            externalWizardFactory.actionFile(file, type).then(function (response) {
                if (response.status == 200) {


                    $scope.progressbar.complete();
                    Flash.dismiss(info_id);
                    Flash.create('success', file + ' downloaded!', 2000);

                    console.log(response);
                    var anchor = angular.element('<a/>');
                    anchor.css({display: 'none'}); // Make sure it's not visible
                    angular.element(document.body).append(anchor); // Attach to document

                    anchor.attr({
                        href: 'data:attachment/txt;charset=utf-8,' + encodeURI(response.data),
                        target: '_blank',
                        download: response.config.data.file
                    })[0].click();

                    anchor.remove(); // Clean it up afterwards

                }
                // handle exception

            });


        };


    }]);