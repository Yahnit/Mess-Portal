var adminManager = (function () {

    var adminHome = function() {
      $.ajax({
          method: 'get',
          url: '/api/login',
          success: function(res) {
              console.log(res.user);
              viewManager.render('admin_home', {
                  user: res.user,
              }, function($view) {
                  console.log($view)
                });
          }
      });
    }

    var studentAdminHome = function() {
      $.ajax({
          method: 'get',
          url: '/api/login',
          success: function(res) {
              console.log(res.user);
              viewManager.render('student_admin_home', {
                  user: res.user,
                  mess_data:res.details,
              }, function($view) {
                  console.log($view)
                });
          }
      });
    }

    // var helloadmin = function() {
    //   console.log("in helloadmin function");
    //   viewManager.render('admin_home',function($view) {
    //     console.log($view);
    //   });
    // }
    //
    // var hi = function() {
    //   console.log("in hi function");
    //   viewManager.render('student_admin_home',function($view) {
    //     console.log($view);
    //   });
    // }

    var inactiveList = function() {
      $.ajax({
          method: 'get',
          url: '/api/inactive_students',
          success: function(res) {
              console.log(res.users);
              viewManager.render('inactive-list', {
                  users: res.users,
              }, function($view) {
                  $view.find(".activate-user").click(activateUserForm);
              });
          }
      });
    }

    var activateUserForm = function() {
      console.log("in activate form");
      console.log($(this).data('id'));
      student_roll = $(this).data('id');

      viewManager.render('activateStudent',{rollno:student_roll},
      function($view) {
        $view.submitViaAjax(function (response) {
          $('form').html("");
          page('/inactive-list');
        });
      },'form');
    }

    var activeList = function() {
      $.ajax({
          method: 'get',
          url: '/api/active_students',
          success: function(res) {
              console.log(res.users);
              viewManager.render('active-list', {
                  users: res.users,
              }, function($view) {
                  $view.find(".deactivate-user").click(
                    function() {
                      student_roll = $(this).data('id');
                      $.ajax({
                        method:'post',
                        url: 'api/deactivate_student',
                        data: {
                          rollno:student_roll,
                        },
                        success: function(response){
                          page('/active-list')
                        },
                      })
                    });
              });
          }
      });
    }

    var viewStudent = function() {
        viewManager.render('forms/view-student',
        function($view) {
          $view.submitViaAjax(function (response) {
            viewManager.render('view-student-details',{student:response.student},
            function($view){

              $view.submitViaAjax(function(response) {
                page('/view-student');
              })
            },"getDetails")
            }
          )
        });
    }

    var viewRegistration = function() {
      viewManager.render('view-registration',
      function($view) {
        $view.submitViaAjax(function (response) {
          console.log(response.registration);
          viewManager.render('calender', {
              data: response.registration,
          }, function($view) {
            console.log($view);
          },'calender');
        });
      });
    }

    var resetPassword = function() {
      viewManager.render('reset-password',
        function($view) {
          $view.submitViaAjax(function (response) {
            if(response.success) {
              // $view.find('.message').text(response.message);
              console.log("Password Reset successfully");
              page('/reset-password');
            }
            else {
              $view.find('.message').text(response.message);
            }
          })
        })
    }

    var addStudentAdmin = function() {
      viewManager.render('add-student-admin',
        function($view) {
          $view.submitViaAjax(function(response) {
            if(response.success) {
              page('/add-student-admin');
            }
            else {
              $view.find('.message').text(response.message);
            }
          })
        })
    }

    var viewMessBill = function() {
      viewManager.render('view-mess-bill',
        function($view) {
          $view.submitViaAjax(
            function (response) {
              viewManager.render('view-mess-bill-details',{bill:response.bill},
                function($view){
                  console.log($view)
                }
                ,"messbill")}
          )});
    }

    var viewStudentBill = function() {
      viewManager.render('view-student-bill',
        function($view) {
          $view.submitViaAjax(
            function (response) {
              viewManager.render('view-student-bill-details',{bill:response.bill},
                function($view){
                  console.log($view)
                }
                ,"studentbill")}
          )});
    }

    var updateMess = function() {
      viewManager.render('update-mess',
        function($view) {
          $view.submitViaAjax(
            function(response) {
              if(response.success) {
                page('/update-mess')
              }
              else {
                $view.find('.message').text(response.message);
              }
            }
          )
        })
    }

    var complaints = function() {
      $.ajax({
          method: 'get',
          url: '/api/complaints',
          success: function(res) {
              viewManager.render('complaints', {
                  unresolved: res.unresolved,
                  resolved: res.resolved,
              }, function($view) {
                  $view.find(".resolve-complaint").click(
                    function() {
                      complaint_id = $(this).data('id');
                      $.ajax({
                        method:'post',
                        url: 'api/complaint-resolved',
                        data: {
                          complaint_id:complaint_id,
                        },
                        success: function(response){
                          page('/complaints')
                        },
                      })
                    });
              });
          }
      });
    }
    var changeRegistration = function() {
       viewManager.render('change-registration',
           function($view) {
              $('#date_wise').find('form').submitViaAjax(function(response) {
              if(response.success) {
              page('/change-registration');
              }
              else {
                 $view.find('.date_wise_message').text(response.message);
              }
          })
          $('#day_wise').find('form').submitViaAjax(function(response) {
            if(response.success) {
            page('/change-registration');
            }
            else {
               $view.find('.day_wise_message').text(response.message);
            }
        })
        $('#month_wise').find('form').submitViaAjax(function(response) {
          if(response.success) {
          page('/change-registration');
          }
          else {
             $view.find('.monthly_message').text(response.message);
          }
      })
        })
    }
    var viewDaily = function() {
      viewManager.render('view-daily',
      function($view) {
        $view.submitViaAjax(function (response) {
          console.log(response.users);
          viewManager.render('list_users', {
              data: response.users,
          }, function($view) {
            console.log($view);
          },'list_users');
        });
      });
    }
    var cancelMess = function() {
      viewManager.render('cancel-mess',
      function($view) {
        $view.submitViaAjax(function (response) {
          if(response.success)
          {
            page('/cancel-mess');
          }
          else {
            $view.find('.message').text(response.message);
          }
        });
      });
    }
    var monthlyRegistration = function() {
      viewManager.render('monthly_registration',
      function($view) {
        $view.submitViaAjax(function (response) {
          console.log(response.users);
          viewManager.render('view-monthly-students', {
              data: response.users
          }, function($view) {
            console.log($view);
          },'monthly_students');
        });
      });
    }

    var aManager = {};
    aManager.inactiveList = inactiveList;
    aManager.activateUserForm = activateUserForm;
    aManager.adminHome = adminHome;
    aManager.activeList = activeList;
    aManager.viewStudent = viewStudent;
    aManager.viewRegistration = viewRegistration;
    aManager.resetPassword = resetPassword;
    aManager.addStudentAdmin = addStudentAdmin;
    aManager.studentAdminHome = studentAdminHome;
    aManager.viewMessBill = viewMessBill;
    aManager.viewStudentBill = viewStudentBill;
    aManager.updateMess = updateMess;
    aManager.complaints = complaints;
    aManager.changeRegistration = changeRegistration;
    aManager.viewDaily = viewDaily;
    aManager.cancelMess = cancelMess;
    aManager.monthlyRegistration = monthlyRegistration;
    return aManager;
})();
