var app = angular.module('schemaApp');


app.controller('listController', [
    '$scope',
    'Flash',
    'listFactory',
    '$state',
    function ($scope,
              Flash,
              listFactory,
              $state) {

        var customer = $state.params.customer_shortcut;
        $scope.progressbar.start();

        listFactory.getList(customer).then(function (response) {
            if (response.data.success) {
                data = response.data.data;
                $scope.folders = data.folders;
                $scope.customer = data.customer;
                $scope.objects = data.objects;
                $scope.prefix = data.prefix;
                $scope.not_front = data.not_front;
                $scope.progressbar.complete();
            }
        });


        $scope.navigate = function (element) {
            var prefix;
            var back = false;

            $scope.progressbar.start();
            if (element) {
                prefix = element.target.value;
            }
            else {
                prefix = $scope.prefix;
                back = true;
            }

            listFactory.getList(customer, prefix, back).then(function (response) {
                if (response.data.success) {
                    data = response.data.data;
                    $scope.folders = data.folders;
                    $scope.customer = data.customer;
                    $scope.objects = data.objects;
                    $scope.prefix = data.prefix;
                    $scope.front = data.front;
                    $scope.progressbar.complete();
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

        $scope.download = function (element){

            var object = element.currentTarget.value;
            var customer = $scope.customer;

            $scope.progressbar.start();
            var flash_msg = "<b> Downloading " + object;
            var info_id = Flash.create('info', flash_msg , 0, false);

            listFactory.download(customer, object).then(function (response) {
                if (response.status == 200) {
                    $scope.progressbar.complete();
                    Flash.dismiss(info_id);
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
            });
        };


        $scope.search = function () {
            var regex = $scope.regex;
            var customer = $scope.customer;

            $scope.progressbar.start();
            var flash_msg = "<b> Searching for " + regex + " .. This might take a while.. ";
            var info_id = Flash.create('info', flash_msg , 0, false);

            listFactory.search(regex, customer).then(function (response) {
                if (response.data.success)
                    $scope.progressbar.complete();
                    Flash.dismiss(info_id);
                    $scope.folders = [];
                    $scope.front = false;
                    data = response.data.data;
                    $scope.objects = data.objects;
                    flash_msg = "<b> Success! Found "
                                + data.objects.length
                                + " object(s) that matchs "
                                + regex;
                    Flash.create('success', flash_msg);
            });

        };


    }]);