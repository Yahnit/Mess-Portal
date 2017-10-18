page('/', authManager.showHome);

page('/logout', authManager.logout);

page('/guest',authManager.allowOnlyGuest,authManager.guestHome)

page('/student',authManager.requiresAuthenticationStudent,studentManager.studentHome)
page('/student-view-registration',authManager.requiresAuthenticationStudent,studentManager.viewRegistration)
page('/student-change-registration',authManager.requiresAuthenticationStudent,studentManager.changeRegistration)
page('/student-default-mess',authManager.requiresAuthenticationStudent,studentManager.defaultMess)
page('/my-complaints',authManager.requiresAuthenticationStudent,studentManager.complaints)
page('/student-cancel-meals',authManager.requiresAuthenticationStudent,studentManager.cancelMeals)
page('/student-uncancel-meals',authManager.requiresAuthenticationStudent,studentManager.uncancelMeals)
page('/student-bill',authManager.requiresAuthenticationStudent,studentManager.viewStudentBill)

page('/admin',authManager.requiresAuthenticationAdmin,adminManager.adminHome)
page('/inactive-list',authManager.requiresAuthenticationAdmin,adminManager.inactiveList)
page('/active-list',authManager.requiresAuthenticationAdmin,adminManager.activeList)
page('/view-student',authManager.requiresAuthenticationAdmin,adminManager.viewStudent)
page('/view-registration',authManager.requiresAuthenticationAdmin,adminManager.viewRegistration)
page('/reset-password',authManager.requiresAuthenticationAdmin,adminManager.resetPassword)
page('/add-student-admin',authManager.requiresAuthenticationAdmin,adminManager.addStudentAdmin)
page('/view-mess-bill',authManager.requiresAuthenticationAdmin,adminManager.viewMessBill)
page('/view-student-bill',authManager.requiresAuthenticationAdmin,adminManager.viewStudentBill)
page('/update-mess',authManager.requiresAuthenticationAdmin,adminManager.updateMess)
page('/complaints',authManager.requiresAuthenticationAdmin,adminManager.complaints)
page('/change-registration',authManager.requiresAuthenticationAdmin,adminManager.changeRegistration)
page('/view_daily_users',authManager.requiresAuthenticationAdmin,adminManager.viewDaily)
page('/cancel-mess',authManager.requiresAuthenticationAdmin,adminManager.cancelMess)
page('/monthly-registration',authManager.requiresAuthenticationAdmin,adminManager.monthlyRegistration)


page('/student_admin',authManager.requiresAuthenticationAdmin,adminManager.studentAdminHome)

page({});
