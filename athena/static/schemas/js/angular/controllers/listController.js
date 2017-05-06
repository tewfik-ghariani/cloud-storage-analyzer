var app = angular.module('schemaApp');


app.controller('listController', [
    '$scope',
    'Flash',
    '$rootScope',
    'listFactory',
    '$state',
    function ($scope,
              Flash,
              $rootScope,
              listFactory,
              $state) {

        $rootScope.customer = $state.params.customer_shortcut || $rootScope.customer ;
        var customer = $rootScope.customer || $scope.customer;

        $scope.arrived = false;
        $scope.progressbar.start();

        listFactory.getList(customer).then(function (response) {
            $scope.progressbar.complete();

            if (response.data.success) {
                data = response.data.data;
                $scope.folders = data.folders;
                $scope.objects = data.objects;
                $scope.prefix = data.prefix;
                $scope.not_front = data.not_front;
                $scope.arrived = true;
            }
            else {
                Flash.create('danger', response.data.error, false);
            }
        });


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

            listFactory.getList(customer, prefix, back).then(function (response) {
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


        $scope.configGet = function (element) {
            var object = element.target.value;
            var customer = $scope.customer;
            $state.go('config', params = {
                'customer': customer,
                'object': object
            })


        };

        $scope.download = function (element) {
            var object = element.currentTarget.value;
            var customer = $scope.customer;

            var flash_msg = "<b> Downloading " + object;
            var info_id = Flash.create('info', flash_msg, 0, false);
            $scope.progressbar.start();

            listFactory.download(customer, object).then(function (response) {
                $scope.progressbar.complete();
                Flash.dismiss(info_id);

                if (response.status == 200) {
                    flash_msg = "<b> Success! " + object + " successfully downloaded! ";
                    Flash.create('success', flash_msg);

                    var anchor = angular.element('<a/>');
                    anchor.css({display: 'none'}); // Make sure it's not visible
                    angular.element(document.body).append(anchor); // Attach to document

                    anchor.attr({
                        href: 'data:attachment/txt;charset=utf-8,' + encodeURI(response.data),
                        target: '_blank',
                        download: response.config.data.object
                    })[0].click();

                    anchor.remove(); // Clean it up afterwards
                }
                else if (response.status == 201) {
                    Flash.create('danger', 'Error in download');
                }
            });
        };


        $scope.search = function () {
            var regex = $scope.regex;
            var customer = $scope.customer;

            var flash_msg = "<b> Searching for " + regex + " .. This might take a while.. ";
            var info_id = Flash.create('info', flash_msg, 0, false);
            $scope.progressbar.start();

            listFactory.search(regex, customer).then(function (response) {
                $scope.progressbar.complete();
                Flash.dismiss(info_id);

                if (response.data.success) {
                    $scope.folders = [];
                    $scope.front = false;
                    data = response.data.data;
                    $scope.objects = data.objects;
                    flash_msg = "<b> Success! Found "
                        + data.objects.length
                        + " object(s) that matchs "
                        + regex;
                    Flash.create('success', flash_msg);
                }
                else {
                    Flash.create('danger', response.data.error, false);
                }
            });
        };

    }]);