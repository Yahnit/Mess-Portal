var authManager = (function() {
    var loginState = null;
    var intendedPath = null;

    var loggedIn = function (user,type) {
        loginState = {};
        loginState.loggedIn = true;
        loginState.user = user;
        loginState.type = type;
        if(intendedPath) page(intendedPath);
        else showHome();
    };

    var showHome = function(ctx,next) {
      getLoginState(function (state) {
            if(state == null) {
              page('/guest');
            }
            else if(!state.loggedIn) {
              page('/guest');
            }
            else if (state.type == 'admin') {
              console.log("admin");
                page('/admin');
            }
            else if(state.type == 'student') {
                page('/student');
            }
            else if(state.type == 'student_admin'){
              page('/student_admin');
            }
      })
    }

    var getLoginState = function (cb) {
        if (loginState === null) {
            $.get({
                url: '/api/login',
                success: function (response) {
                    loginState = {};
                    if (response.success) {
                        loginState.loggedIn = true;
                        loginState.user = response.user;
                        loginState.type = response.type;
                    } else {
                        loginState.loggedIn = false;
                    }
                    cb(loginState);
                },
                error: function (response) {
                    cb(loginState);
                }
            });
        } else {
            cb(loginState);
        }
    };

    var requiresAuthenticationStudent = function(ctx, next) {
        getLoginState(function (state) {
            if (state && state.loggedIn && (state.type=='student' || state.type=='student_admin')) {
                next();
            } else {
                intendedPath = ctx.path;
                page('/');
            }
        });
    };

    var requiresAuthenticationAdmin = function(ctx, next) {
        getLoginState(function (state) {
            console.log(state);
            if (state && state.loggedIn && (state.type=='admin' || state.type=='student_admin')) {
                next();
            } else {
                intendedPath = ctx.path;
                page('/login');
            }
        });
    };

    var allowOnlyGuest = function (ctx, next) {
        getLoginState(function (state) {
            if (state.loggedIn) {
                page('/');
            } else {
                next();
            }
        });
    };

    var guestHome = function() {
        viewManager.render('guest/home', function ($view) {
          $view
          .find('#login-form')
          .find('form')
          .submitViaAjax(function (response) {
            if (response.success) {
              loggedIn(response.user,response.type);
              $(".modal-backdrop.fade.in").remove();
              displayMessage({"message":"Successfully logged In","type":"success"})
            }
            else {
              displayMessage({"message":response.message,"type":response.type},'login-form-message');
            }
          });
          $view
          .find('#register-form')
          .find('form')
          .submitViaAjax(function (registerResponse) {
            var form = this;
            if (registerResponse.success) {
                $.post({
                    url: '/api/login',
                    data: {
                        email: form.email.value,
                        password: form.password.value,
                    },
                    success: function(response) {
                        if (response.success) {
                            loggedIn(response.user,response.type);
                            $(".modal-backdrop.fade.in").remove();
                        } else {
                            path('/');
                            displayMessage({"message":"Please login to continue","type":"info"})
                        }
                    },
                })
            }
            else {
              displayMessage({"message":registerResponse.message,"type":registerResponse.type},'register-form-message');
            }
          });
      });
    }

    var logout = function () {
      intendedPath=null;
        $.post({
            url: '/api/logout',
            success: function (response) {
                loginState = null;
                page("/");
                displayMessage({"message":"Successfully Logged out","type":"success"})
            },
        });
    }


    var aManager = {};
    aManager.guestHome = guestHome;
    aManager.logout = logout;
    aManager.showHome = showHome;
    aManager.allowOnlyGuest = allowOnlyGuest;
    aManager.requiresAuthenticationStudent = requiresAuthenticationStudent;
    aManager.requiresAuthenticationAdmin = requiresAuthenticationAdmin;
    return aManager;
})();
