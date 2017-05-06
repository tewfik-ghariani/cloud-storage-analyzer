var app = angular.module('wizardApp');


app.controller('externalController', [
    '$scope',
    'externalWizardFactory',
    'Flash',
    function ($scope,
              externalWizardFactory,
              Flash) {


        $scope.progressbar.start();

        externalWizardFactory.getObjects().then(function (response) {
            $scope.progressbar.complete();

            if (response.data.success) {
                data = response.data.data;
                $scope.folders = data.folders;
                $scope.objects = data.objects;
                $scope.front = false;
            }
            else {
                Flash.create('danger', response.data.error, false);
            }
        });


        $scope.delete = function (element, object_id) {
            file = element.currentTarget.value;
            fetch = element.currentTarget.name;

            var info_id = Flash.create('danger', "<b> Deleting file.. </b>" + file, 0, false);
            $scope.progressbar.start();

            externalWizardFactory.actionFile(file, fetch).then(function (response) {
                $scope.progressbar.complete();
                Flash.dismiss(info_id);

                if (response.data.success) {
                    $scope.objects.splice(object_id, 1);
                    Flash.create('success', file + ' deleted!', 2000);
                }
                else {
                    Flash.create('danger', response.data.error, false);
                }
            });
        };


        $scope.download = function (element) {
            file = element.currentTarget.value;
            fetch = element.currentTarget.name;
            var info_id = Flash.create('info', "<b> Downloading file.. </b>" + file, 0, false);
            $scope.progressbar.start();

            externalWizardFactory.actionFile(file, fetch).then(function (response) {
                $scope.progressbar.complete();
                Flash.dismiss(info_id);

                if (response.status == 200) {
                    Flash.create('success', file + ' downloaded!', 2000);

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
                else if (response.status == 201) {
                    Flash.create('danger', 'Error in download');
                }
            });
        };


        $scope.navigate = function (element) {
            var prefix;
            var back = false;

            if (element) {
                prefix = element.target.value;
            }
            else {
                prefix = $scope.prefix;
                back = true;
            }
            $scope.progressbar.start();

            externalWizardFactory.getObjects(prefix, back).then(function (response) {
                $scope.progressbar.complete();

                if (response.data.success) {
                    data = response.data.data;
                    $scope.folders = data.folders;
                    $scope.objects = data.objects;
                    $scope.prefix = data.prefix;
                    $scope.front = data.front;
                }
                else {
                    Flash.create('danger', response.data.error, false);
                }
            });
        };


    }]);