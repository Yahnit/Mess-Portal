$.fn.submitViaAjax = function (success, error) {
    this.on('submit', function (e) {
        e.preventDefault();
        var form = this;
        $.ajax({
            method: form.method,
            url: form.action,
            data: $(form).serialize(),
            success: success ? success.bind(form) : function () {},
            error: error? error.bind(form) : function () {},
        });
        return false;
    });
    return this;
};

var displayMessage = function(response,id) {
  if(id) {
    viewManager.render('utilities/message',{message:response.message,type:response.type,},function($view){},id);
  }
  else {
    viewManager.render('utilities/message',{message:response.message,type:response.type,},function($view){},'message-container');
  }
}
