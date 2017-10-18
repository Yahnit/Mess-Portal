var viewManager = (function () {
    var vm = {};
    var templateCache = {};
    var $root = $('#content');

    var renderTemplate = function (template, data, callback,elementId) {
        var compiledTemplate = Handlebars.compile(template);
        var renderedHtml = compiledTemplate(data);
        var $node = $(renderedHtml);
        if(!elementId) {
          $root.html( $node );
        }
        else {
          $('#'+elementId).html($node);
        }
        // $root.html( "hello" );

        if ($.isFunction(callback)) {
            callback($node);
        }
    };

    var render = function(view, data, callback,elementId) {

        if ($.isFunction(data)) {
            callback = data;
            data = {};
        }
        if (view in templateCache) {
            renderTemplate(templateCache[view], data, callback,elementId);
        }
        $.get({
            url:'/static/templates/' + view + '.html',
            success: function (response) {
                templateCache[view] = response;
                renderTemplate(response, data, callback,elementId);
            }
        });
    };

    vm.render = render;
    return vm;
})();
