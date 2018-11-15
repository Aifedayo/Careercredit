(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["main"],{

/***/ "./src/$$_lazy_route_resource lazy recursive":
/*!**********************************************************!*\
  !*** ./src/$$_lazy_route_resource lazy namespace object ***!
  \**********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncaught exception popping up in devtools
	return Promise.resolve().then(function() {
		var e = new Error("Cannot find module '" + req + "'");
		e.code = 'MODULE_NOT_FOUND';
		throw e;
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "./src/$$_lazy_route_resource lazy recursive";

/***/ }),

/***/ "./src/app/app-routing.module.ts":
/*!***************************************!*\
  !*** ./src/app/app-routing.module.ts ***!
  \***************************************/
/*! exports provided: AppRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppRoutingModule", function() { return AppRoutingModule; });
/* harmony import */ var _linux_linux_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./linux/linux.component */ "./src/app/linux/linux.component.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _home_home_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./home/home.component */ "./src/app/home/home.component.ts");
/* harmony import */ var _signup_signup_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./signup/signup.component */ "./src/app/signup/signup.component.ts");
/* harmony import */ var _login_login_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./login/login.component */ "./src/app/login/login.component.ts");
/* harmony import */ var _course_course_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./course/course.component */ "./src/app/course/course.component.ts");
/* harmony import */ var _auth_guard__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./auth.guard */ "./src/app/auth.guard.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};








var routes = [
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'classroom', component: _course_course_component__WEBPACK_IMPORTED_MODULE_6__["CourseComponent"], canActivate: [_auth_guard__WEBPACK_IMPORTED_MODULE_7__["AuthGuard"]] },
    { path: 'linux', component: _linux_linux_component__WEBPACK_IMPORTED_MODULE_0__["LinuxComponent"], canActivate: [_auth_guard__WEBPACK_IMPORTED_MODULE_7__["AuthGuard"]] },
    { path: 'signup', component: _signup_signup_component__WEBPACK_IMPORTED_MODULE_4__["SignupComponent"] },
    { path: 'login', component: _login_login_component__WEBPACK_IMPORTED_MODULE_5__["LoginComponent"] },
    { path: 'home', component: _home_home_component__WEBPACK_IMPORTED_MODULE_3__["HomeComponent"] },
];
var AppRoutingModule = /** @class */ (function () {
    function AppRoutingModule() {
    }
    AppRoutingModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
            imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forRoot(routes)],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
            providers: [_auth_guard__WEBPACK_IMPORTED_MODULE_7__["AuthGuard"]]
        })
    ], AppRoutingModule);
    return AppRoutingModule;
}());



/***/ }),

/***/ "./src/app/app.component.css":
/*!***********************************!*\
  !*** ./src/app/app.component.css ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/app.component.html":
/*!************************************!*\
  !*** ./src/app/app.component.html ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<router-outlet></router-outlet>\n"

/***/ }),

/***/ "./src/app/app.component.ts":
/*!**********************************!*\
  !*** ./src/app/app.component.ts ***!
  \**********************************/
/*! exports provided: AppComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppComponent", function() { return AppComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};

var AppComponent = /** @class */ (function () {
    function AppComponent() {
        this.title = 'DjangoClass';
    }
    AppComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-root',
            template: __webpack_require__(/*! ./app.component.html */ "./src/app/app.component.html"),
            styles: [__webpack_require__(/*! ./app.component.css */ "./src/app/app.component.css")]
        })
    ], AppComponent);
    return AppComponent;
}());



/***/ }),

/***/ "./src/app/app.module.ts":
/*!*******************************!*\
  !*** ./src/app/app.module.ts ***!
  \*******************************/
/*! exports provided: AppModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppModule", function() { return AppModule; });
/* harmony import */ var _course_topic_detail_topic_detail_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./course/topic-detail/topic-detail.component */ "./src/app/course/topic-detail/topic-detail.component.ts");
/* harmony import */ var _linux_linux_chat_linux_chat_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./linux/linux-chat/linux-chat.component */ "./src/app/linux/linux-chat/linux-chat.component.ts");
/* harmony import */ var _linux_linux_routing_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./linux/linux-routing.module */ "./src/app/linux/linux-routing.module.ts");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm5/platform-browser.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm5/forms.js");
/* harmony import */ var ng2_file_upload__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ng2-file-upload */ "./node_modules/ng2-file-upload/index.js");
/* harmony import */ var ng2_file_upload__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(ng2_file_upload__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @angular/platform-browser/animations */ "./node_modules/@angular/platform-browser/fesm5/animations.js");
/* harmony import */ var mat_video__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! mat-video */ "./node_modules/mat-video/esm5/mat-video.js");
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./app.component */ "./src/app/app.component.ts");
/* harmony import */ var _signup_signup_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./signup/signup.component */ "./src/app/signup/signup.component.ts");
/* harmony import */ var _home_home_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./home/home.component */ "./src/app/home/home.component.ts");
/* harmony import */ var _login_login_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./login/login.component */ "./src/app/login/login.component.ts");
/* harmony import */ var _course_videos_videos_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./course/videos/videos.component */ "./src/app/course/videos/videos.component.ts");
/* harmony import */ var _course_video2_video2_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./course/video2/video2.component */ "./src/app/course/video2/video2.component.ts");
/* harmony import */ var _course_video3_video3_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./course/video3/video3.component */ "./src/app/course/video3/video3.component.ts");
/* harmony import */ var _course_video4_video4_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./course/video4/video4.component */ "./src/app/course/video4/video4.component.ts");
/* harmony import */ var _course_video5_video5_component__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./course/video5/video5.component */ "./src/app/course/video5/video5.component.ts");
/* harmony import */ var _course_video6_video6_component__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./course/video6/video6.component */ "./src/app/course/video6/video6.component.ts");
/* harmony import */ var _course_video7_video7_component__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./course/video7/video7.component */ "./src/app/course/video7/video7.component.ts");
/* harmony import */ var _course_video8_video8_component__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./course/video8/video8.component */ "./src/app/course/video8/video8.component.ts");
/* harmony import */ var _course_video9_video9_component__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./course/video9/video9.component */ "./src/app/course/video9/video9.component.ts");
/* harmony import */ var _course_video10_video10_component__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./course/video10/video10.component */ "./src/app/course/video10/video10.component.ts");
/* harmony import */ var _course_video11_video11_component__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ./course/video11/video11.component */ "./src/app/course/video11/video11.component.ts");
/* harmony import */ var _course_labs_labs_component__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ./course/labs/labs.component */ "./src/app/course/labs/labs.component.ts");
/* harmony import */ var _course_topic_chat_component__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ./course/topic-chat.component */ "./src/app/course/topic-chat.component.ts");
/* harmony import */ var _course_course_component__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(/*! ./course/course.component */ "./src/app/course/course.component.ts");
/* harmony import */ var angular2_materialize__WEBPACK_IMPORTED_MODULE_28__ = __webpack_require__(/*! angular2-materialize */ "./node_modules/angular2-materialize/dist/index.js");
/* harmony import */ var _course_course_routing_module__WEBPACK_IMPORTED_MODULE_29__ = __webpack_require__(/*! ./course/course-routing.module */ "./src/app/course/course-routing.module.ts");
/* harmony import */ var _app_routing_module__WEBPACK_IMPORTED_MODULE_30__ = __webpack_require__(/*! ./app-routing.module */ "./src/app/app-routing.module.ts");
/* harmony import */ var _course_video12_video12_component__WEBPACK_IMPORTED_MODULE_31__ = __webpack_require__(/*! ./course/video12/video12.component */ "./src/app/course/video12/video12.component.ts");
/* harmony import */ var _course_video13_video13_component__WEBPACK_IMPORTED_MODULE_32__ = __webpack_require__(/*! ./course/video13/video13.component */ "./src/app/course/video13/video13.component.ts");
/* harmony import */ var _course_video14_video14_component__WEBPACK_IMPORTED_MODULE_33__ = __webpack_require__(/*! ./course/video14/video14.component */ "./src/app/course/video14/video14.component.ts");
/* harmony import */ var _course_video15_video15_component__WEBPACK_IMPORTED_MODULE_34__ = __webpack_require__(/*! ./course/video15/video15.component */ "./src/app/course/video15/video15.component.ts");
/* harmony import */ var _course_video16_video16_component__WEBPACK_IMPORTED_MODULE_35__ = __webpack_require__(/*! ./course/video16/video16.component */ "./src/app/course/video16/video16.component.ts");
/* harmony import */ var _course_video17_video17_component__WEBPACK_IMPORTED_MODULE_36__ = __webpack_require__(/*! ./course/video17/video17.component */ "./src/app/course/video17/video17.component.ts");
/* harmony import */ var _course_video18_video18_component__WEBPACK_IMPORTED_MODULE_37__ = __webpack_require__(/*! ./course/video18/video18.component */ "./src/app/course/video18/video18.component.ts");
/* harmony import */ var _course_video19_video19_component__WEBPACK_IMPORTED_MODULE_38__ = __webpack_require__(/*! ./course/video19/video19.component */ "./src/app/course/video19/video19.component.ts");
/* harmony import */ var _course_private_chat_private_chat_component__WEBPACK_IMPORTED_MODULE_39__ = __webpack_require__(/*! ./course/private-chat/private-chat.component */ "./src/app/course/private-chat/private-chat.component.ts");
/* harmony import */ var _course2_course2_component__WEBPACK_IMPORTED_MODULE_40__ = __webpack_require__(/*! ./course2/course2.component */ "./src/app/course2/course2.component.ts");
/* harmony import */ var _linux_linux_component__WEBPACK_IMPORTED_MODULE_41__ = __webpack_require__(/*! ./linux/linux.component */ "./src/app/linux/linux.component.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};










































var AppModule = /** @class */ (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_4__["NgModule"])({
            declarations: [
                _app_component__WEBPACK_IMPORTED_MODULE_10__["AppComponent"],
                ng2_file_upload__WEBPACK_IMPORTED_MODULE_7__["FileSelectDirective"],
                _linux_linux_chat_linux_chat_component__WEBPACK_IMPORTED_MODULE_1__["LinuxChatComponent"],
                _linux_linux_component__WEBPACK_IMPORTED_MODULE_41__["LinuxComponent"],
                _signup_signup_component__WEBPACK_IMPORTED_MODULE_11__["SignupComponent"],
                _home_home_component__WEBPACK_IMPORTED_MODULE_12__["HomeComponent"],
                _login_login_component__WEBPACK_IMPORTED_MODULE_13__["LoginComponent"],
                _course_course_component__WEBPACK_IMPORTED_MODULE_27__["CourseComponent"],
                _course_videos_videos_component__WEBPACK_IMPORTED_MODULE_14__["VideosComponent"],
                _course_video2_video2_component__WEBPACK_IMPORTED_MODULE_15__["Video2Component"],
                _course_video3_video3_component__WEBPACK_IMPORTED_MODULE_16__["Video3Component"],
                _course_labs_labs_component__WEBPACK_IMPORTED_MODULE_25__["LabsComponent"],
                _course_topic_chat_component__WEBPACK_IMPORTED_MODULE_26__["TopicChatComponent"],
                _course_video4_video4_component__WEBPACK_IMPORTED_MODULE_17__["Video4Component"],
                _course_video5_video5_component__WEBPACK_IMPORTED_MODULE_18__["Video5Component"],
                _course_video6_video6_component__WEBPACK_IMPORTED_MODULE_19__["Video6Component"],
                _course_video7_video7_component__WEBPACK_IMPORTED_MODULE_20__["Video7Component"],
                _course_video8_video8_component__WEBPACK_IMPORTED_MODULE_21__["Video8Component"],
                _course_video9_video9_component__WEBPACK_IMPORTED_MODULE_22__["Video9Component"],
                _course_video10_video10_component__WEBPACK_IMPORTED_MODULE_23__["Video10Component"],
                _course_video11_video11_component__WEBPACK_IMPORTED_MODULE_24__["Video11Component"],
                _course_video12_video12_component__WEBPACK_IMPORTED_MODULE_31__["Video12Component"],
                _course_video13_video13_component__WEBPACK_IMPORTED_MODULE_32__["Video13Component"],
                _course_video14_video14_component__WEBPACK_IMPORTED_MODULE_33__["Video14Component"],
                _course_video15_video15_component__WEBPACK_IMPORTED_MODULE_34__["Video15Component"],
                _course_video16_video16_component__WEBPACK_IMPORTED_MODULE_35__["Video16Component"],
                _course_video17_video17_component__WEBPACK_IMPORTED_MODULE_36__["Video17Component"],
                _course_video18_video18_component__WEBPACK_IMPORTED_MODULE_37__["Video18Component"],
                _course_video19_video19_component__WEBPACK_IMPORTED_MODULE_38__["Video19Component"],
                _course_private_chat_private_chat_component__WEBPACK_IMPORTED_MODULE_39__["PrivateChatComponent"],
                _course2_course2_component__WEBPACK_IMPORTED_MODULE_40__["Course2Component"],
                _course_topic_detail_topic_detail_component__WEBPACK_IMPORTED_MODULE_0__["TopicDetailComponent"]
            ],
            imports: [
                _angular_platform_browser__WEBPACK_IMPORTED_MODULE_3__["BrowserModule"],
                _angular_common_http__WEBPACK_IMPORTED_MODULE_5__["HttpClientModule"],
                _angular_forms__WEBPACK_IMPORTED_MODULE_6__["FormsModule"],
                _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_8__["BrowserAnimationsModule"],
                mat_video__WEBPACK_IMPORTED_MODULE_9__["MatVideoModule"],
                angular2_materialize__WEBPACK_IMPORTED_MODULE_28__["MaterializeModule"],
                _linux_linux_routing_module__WEBPACK_IMPORTED_MODULE_2__["LinuxRoutingModule"],
                _course_course_routing_module__WEBPACK_IMPORTED_MODULE_29__["CourseRoutingModule"],
                _app_routing_module__WEBPACK_IMPORTED_MODULE_30__["AppRoutingModule"]
            ],
            providers: [],
            bootstrap: [_app_component__WEBPACK_IMPORTED_MODULE_10__["AppComponent"]]
        })
    ], AppModule);
    return AppModule;
}());



/***/ }),

/***/ "./src/app/auth.guard.ts":
/*!*******************************!*\
  !*** ./src/app/auth.guard.ts ***!
  \*******************************/
/*! exports provided: AuthGuard */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AuthGuard", function() { return AuthGuard; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./data.service */ "./src/app/data.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var AuthGuard = /** @class */ (function () {
    function AuthGuard(dataservice, router) {
        this.dataservice = dataservice;
        this.router = router;
    }
    AuthGuard.prototype.canActivate = function (route, state) {
        if (this.dataservice.islogin()) {
            return true;
        }
        else {
            alert('Please Login to Access');
            this.router.navigate(['/login']);
            return false;
        }
    };
    AuthGuard = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_2__["DataService"], _angular_router__WEBPACK_IMPORTED_MODULE_1__["Router"]])
    ], AuthGuard);
    return AuthGuard;
}());



/***/ }),

/***/ "./src/app/course/course-routing.module.ts":
/*!*************************************************!*\
  !*** ./src/app/course/course-routing.module.ts ***!
  \*************************************************/
/*! exports provided: CourseRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CourseRoutingModule", function() { return CourseRoutingModule; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm5/platform-browser.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _course_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./course.component */ "./src/app/course/course.component.ts");
/* harmony import */ var _topic_chat_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./topic-chat.component */ "./src/app/course/topic-chat.component.ts");
/* harmony import */ var _videos_videos_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./videos/videos.component */ "./src/app/course/videos/videos.component.ts");
/* harmony import */ var _video2_video2_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./video2/video2.component */ "./src/app/course/video2/video2.component.ts");
/* harmony import */ var _video3_video3_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./video3/video3.component */ "./src/app/course/video3/video3.component.ts");
/* harmony import */ var _video4_video4_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./video4/video4.component */ "./src/app/course/video4/video4.component.ts");
/* harmony import */ var _video5_video5_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./video5/video5.component */ "./src/app/course/video5/video5.component.ts");
/* harmony import */ var _video6_video6_component__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./video6/video6.component */ "./src/app/course/video6/video6.component.ts");
/* harmony import */ var _video7_video7_component__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./video7/video7.component */ "./src/app/course/video7/video7.component.ts");
/* harmony import */ var _video8_video8_component__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./video8/video8.component */ "./src/app/course/video8/video8.component.ts");
/* harmony import */ var _video9_video9_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./video9/video9.component */ "./src/app/course/video9/video9.component.ts");
/* harmony import */ var _video10_video10_component__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./video10/video10.component */ "./src/app/course/video10/video10.component.ts");
/* harmony import */ var _video11_video11_component__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./video11/video11.component */ "./src/app/course/video11/video11.component.ts");
/* harmony import */ var _video12_video12_component__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./video12/video12.component */ "./src/app/course/video12/video12.component.ts");
/* harmony import */ var _video13_video13_component__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! ./video13/video13.component */ "./src/app/course/video13/video13.component.ts");
/* harmony import */ var _video14_video14_component__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! ./video14/video14.component */ "./src/app/course/video14/video14.component.ts");
/* harmony import */ var _video15_video15_component__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! ./video15/video15.component */ "./src/app/course/video15/video15.component.ts");
/* harmony import */ var _video16_video16_component__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! ./video16/video16.component */ "./src/app/course/video16/video16.component.ts");
/* harmony import */ var _video17_video17_component__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! ./video17/video17.component */ "./src/app/course/video17/video17.component.ts");
/* harmony import */ var _video18_video18_component__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! ./video18/video18.component */ "./src/app/course/video18/video18.component.ts");
/* harmony import */ var _video19_video19_component__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! ./video19/video19.component */ "./src/app/course/video19/video19.component.ts");
/* harmony import */ var _labs_labs_component__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! ./labs/labs.component */ "./src/app/course/labs/labs.component.ts");
/* harmony import */ var _private_chat_private_chat_component__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! ./private-chat/private-chat.component */ "./src/app/course/private-chat/private-chat.component.ts");
/* harmony import */ var _topic_detail_topic_detail_component__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! ./topic-detail/topic-detail.component */ "./src/app/course/topic-detail/topic-detail.component.ts");
/* harmony import */ var _auth_guard__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(/*! ../auth.guard */ "./src/app/auth.guard.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};




























var courseRoutes = [
    {
        path: 'classroom',
        component: _course_component__WEBPACK_IMPORTED_MODULE_3__["CourseComponent"], canActivate: [_auth_guard__WEBPACK_IMPORTED_MODULE_27__["AuthGuard"]],
        children: [
            { path: 'topic-chat', component: _topic_chat_component__WEBPACK_IMPORTED_MODULE_4__["TopicChatComponent"] },
            { path: 'videos', component: _videos_videos_component__WEBPACK_IMPORTED_MODULE_5__["VideosComponent"] },
            {
                path: '',
                children: [
                    { path: 'topic-detail', component: _topic_detail_topic_detail_component__WEBPACK_IMPORTED_MODULE_26__["TopicDetailComponent"] },
                    { path: 'labs', component: _labs_labs_component__WEBPACK_IMPORTED_MODULE_24__["LabsComponent"] },
                    { path: 'private-chat:id', component: _private_chat_private_chat_component__WEBPACK_IMPORTED_MODULE_25__["PrivateChatComponent"],
                        children: [
                            { path: 'id', component: _private_chat_private_chat_component__WEBPACK_IMPORTED_MODULE_25__["PrivateChatComponent"] }
                        ] },
                    { path: 'video2', component: _video2_video2_component__WEBPACK_IMPORTED_MODULE_6__["Video2Component"] },
                    { path: 'video3', component: _video3_video3_component__WEBPACK_IMPORTED_MODULE_7__["Video3Component"] },
                    { path: 'video4', component: _video4_video4_component__WEBPACK_IMPORTED_MODULE_8__["Video4Component"] },
                    { path: 'video5', component: _video5_video5_component__WEBPACK_IMPORTED_MODULE_9__["Video5Component"] },
                    { path: 'video6', component: _video6_video6_component__WEBPACK_IMPORTED_MODULE_10__["Video6Component"] },
                    { path: 'video7', component: _video7_video7_component__WEBPACK_IMPORTED_MODULE_11__["Video7Component"] },
                    { path: 'video8', component: _video8_video8_component__WEBPACK_IMPORTED_MODULE_12__["Video8Component"] },
                    { path: 'video9', component: _video9_video9_component__WEBPACK_IMPORTED_MODULE_13__["Video9Component"] },
                    { path: 'video10', component: _video10_video10_component__WEBPACK_IMPORTED_MODULE_14__["Video10Component"] },
                    { path: 'video11', component: _video11_video11_component__WEBPACK_IMPORTED_MODULE_15__["Video11Component"] },
                    { path: 'video12', component: _video12_video12_component__WEBPACK_IMPORTED_MODULE_16__["Video12Component"] },
                    { path: 'video13', component: _video13_video13_component__WEBPACK_IMPORTED_MODULE_17__["Video13Component"] },
                    { path: 'video14', component: _video14_video14_component__WEBPACK_IMPORTED_MODULE_18__["Video14Component"] },
                    { path: 'video15', component: _video15_video15_component__WEBPACK_IMPORTED_MODULE_19__["Video15Component"] },
                    { path: 'video16', component: _video16_video16_component__WEBPACK_IMPORTED_MODULE_20__["Video16Component"] },
                    { path: 'video17', component: _video17_video17_component__WEBPACK_IMPORTED_MODULE_21__["Video17Component"] },
                    { path: 'video18', component: _video18_video18_component__WEBPACK_IMPORTED_MODULE_22__["Video18Component"] },
                    { path: 'video19', component: _video19_video19_component__WEBPACK_IMPORTED_MODULE_23__["Video19Component"] }
                ]
            }
        ]
    }
];
var CourseRoutingModule = /** @class */ (function () {
    function CourseRoutingModule() {
    }
    CourseRoutingModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["NgModule"])({
            imports: [
                _angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__["BrowserModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forChild(courseRoutes),
            ],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]],
            providers: [_auth_guard__WEBPACK_IMPORTED_MODULE_27__["AuthGuard"]]
        })
    ], CourseRoutingModule);
    return CourseRoutingModule;
}());



/***/ }),

/***/ "./src/app/course/course.component.css":
/*!*********************************************!*\
  !*** ./src/app/course/course.component.css ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\r\n\r\nnav {\r\n    background-color: #6c63ff;\r\n}\r\n\r\nnav ul a:hover {\r\n\r\n  border-bottom: 4px solid #6c63ff;\r\n}\r\n\r\n.logo {\r\n    height: 15%;\r\n    width: 15%;\r\n    margin-top: 17px\r\n    }\r\n\r\n.logo-text {\r\n  position: absolute;\r\n  padding-left: 3px;\r\n  font-weight: 700;\r\n  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\r\n  font-size: 1.4rem;\r\n}\r\n\r\n.dropdown {\r\n  position: absolute;\r\n}\r\n\r\n.dropdown:hover {\r\n  background-color: #6c63ff;\r\n  border-bottom: 4px solid #6c63ff;\r\n}\r\n\r\n.dropdown-content{\r\n    width: -webkit-max-content !important;\r\n    width: -moz-max-content !important;\r\n    width: max-content !important;\r\n    height:auto !important;\r\n }\r\n\r\n#video {\r\n  margin-right: 4px;\r\n  margin-left: 4px;\r\n}\r\n\r\n#lab {\r\n  margin-right: 4px;\r\n  margin-left: 4px;\r\n}\r\n\r\n#chat {\r\n    margin-right: 4px;\r\n    margin-left: 4px;\r\n}\r\n\r\n.lab_area {\r\n    border-radius: 20px;\r\n    border: 2px solid #cdd1d4de;\r\n    height: 400px;\r\n    width: 600px;\r\n    margin-left: 10px;\r\n}\r\n\r\n.course_topic {\r\n    background-color: black;\r\n    height: 35px;\r\n    text-align: center;\r\n    color: aliceblue;\r\n    font-weight: 400;\r\n    margin-top: 0px;\r\n    border-top-right-radius: 20px;\r\n    border-top-left-radius: 20px;\r\n}\r\n\r\n#message_box {\r\n    display: block!important;\r\n    height:1.7rem!important;\r\n    padding: .5rem!important;\r\n    border: 2px solid #636566de;\r\n    transition: all 1s;\r\n    border-radius: .5rem!important;\r\n    box-shadow: none;\r\n    width: 98%!important;\r\n}\r\n\r\n#submit {\r\n    height: 2.9rem!important;\r\n    border-top-right-radius: .5rem;\r\n    border-bottom-right-radius: .5rem;\r\n    -webkit-appearance: none;\r\n       -moz-appearance: none;\r\n            appearance: none;\r\n    margin-left: -50px;\r\n    padding-right: 10px;\r\n    border-right: 2px solid #636566de;\r\n    border-top: 2px solid #636566de;\r\n    border-bottom: 2px solid #636566de;\r\n    box-shadow: none;\r\n    padding-right: 10px;\r\n    padding-left: auto;\r\n    margin-bottom: 0px;\r\n}\r\n\r\n#send_icon {\r\n    margin-left: -10px;\r\n}\r\n"

/***/ }),

/***/ "./src/app/course/course.component.html":
/*!**********************************************!*\
  !*** ./src/app/course/course.component.html ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div class=\"navbar \">\n  <nav>\n    <div class=\"nav-wrapper\">\n      <div class=\"container-fluid\">\n        <div class=\"row\">\n\n          <div class=\"col l3 m3 s3\">\n            <a class=\"brand-logo\"><img src=\"/assets/image/Final-Logo.png\" alt=\"nav-logo\" class=\"logo\"><span class=\"logo-text\">ClassRoom</span></a>\n          </div>\n\n          <div class=\"col l3 m3 s3\">\n            <a materialize=\"dropdown\" class=\"dropdown-button dropdown\" data-activates=\"dropdown1\" style=\"cursor:pointer;\">Django<i class=\"material-icons right\">arrow_drop_down</i></a>\n            <!-- Dropdown Structure -->\n            <ul style=\"cursor: pointer;\" id=\"dropdown1\" class=\"dropdown-content\">\n                <li><a >Django</a></li>\n                <li class=\"divider\"></li>\n                <li><a routerLink=\"/linux\" routerLinkActive>Linux Fundamental</a></li>\n            </ul>\n\n          </div>\n\n            <div class=\"col l6 m6 s6\">\n              <ul class=\"right\">\n                <li><a>{{dataservice.username}}</a></li>\n                <li><a (click)=\"logout()\" id=\"logout\">LOGOUT</a></li>\n              </ul>\n            </div>\n        </div>\n      </div>\n    </div>\n  </nav>\n</div>\n\n<div class=\"container-fluid\">\n  <div class=\"row\">\n    <div class=\"col l3 m3 s3\" style=\"background-color:#4d394b; height: 100%;\">\n      <h6 style=\"text-align: center; font-weight: bold;\">Registered Students | {{users.length}}</h6>\n      <div style=\"height:450px; overflow: auto;\">\n        <ul>\n          <li id=\"students\" style=\"color:darkgrey; font-weight: bolder; font-size: 15px;\"\n              *ngFor=\"let user of users\"><a [routerLink]=\"['./private-chat']\" routerLinkActive=\"active\" > {{ user.username }} </a>\n          </li><br>\n        </ul>\n      </div>\n    </div>\n    <div class=\"col l6 m6 s9\">\n      <ul style=\"display:flex;\">\n        <li><a [routerLink]=\"['./videos']\" routerLinkActive=\"active\" id=\"video\">Video</a></li> |\n        <li><a href= \"http://54.244.162.68:8001/courses/Django/topics/\" target=\"_blank\" id=\"lab\">Labs</a></li> |\n        <li><a [routerLink]=\"['./topic-chat']\" routerLinkActive=\"active\" id=\"chat\"> Chat</a></li>\n      </ul>\n      <hr>\n      <div style=\"max-height:600px; overflow: auto;\">\n        <router-outlet></router-outlet>\n      </div>\n    </div>\n    <div class=\"col l3 m3 s12\">\n      <div class=\"\">\n\n          <h5 style=\"text-align:center; font-weight: bolder;\">Topics</h5>\n          <div class=\"course_topic_area\" style=\"height: 450px; overflow: auto;\">\n\n            <!-- <ul class=\"collection\">\n              <li class=\"collection-item avatar\" *ngFor=\"let topic of topics\">\n                <i class=\"material-icons circle red\">play_arrow</i>\n                <a [routerLink]=\"['/topic-detail']\" routerLinkActive=\"active\">{{ topic.title }}</a>\n              </li>\n            </ul> -->\n          <ul class=\"collection\">\n\n              <li class=\"collection-item avatar\">\n                <i class=\"material-icons circle red\">play_arrow</i>\n\n                <a routerLink=\"./videos\" routerLinkActive=\"active\">Django Definition and Installation</a>\n\n              </li>\n              <li class=\"collection-item avatar\">\n                <i class=\"material-icons circle red\">play_arrow</i>\n\n                <a routerLink=\"./video2\" routerLinkActive=\"active\">Creating Your First Django Project and Your First Django Application</a>\n\n              </li>\n              <li class=\"collection-item avatar\">\n                <i class=\"material-icons circle red\">play_arrow</i>\n\n                <a routerLink=\"./video3\" routerLinkActive=\"active\">Connecting With SQLlite, the Default Django Database System</a>\n\n              </li>\n\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video4\" routerLinkActive=\"active\">Connecting Your Django Application to MySQL Database</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                    <a routerLink=\"./video5\" routerLinkActive=\"active\">Setting Up Django Administrator</a>\n\n                  </li>\n                  <li class=\"collection-item avatar\">\n                    <i class=\"material-icons circle red\">play_arrow</i>\n\n                    <a routerLink=\"./video6\" routerLinkActive=\"active\">Making Your Django Apps Reusable for Other Projects</a>\n\n                  </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video7\" routerLinkActive=\"active\">Creating DJango Views</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video8\" routerLinkActive=\"active\">Using Django to Access and Manipulate Data in the Database</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video9\" routerLinkActive=\"active\">More on Using Django API to Edit Data in Database</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video10\" routerLinkActive=\"active\">Creating Django Views that Accept Arguments</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video11\" routerLinkActive=\"active\">Creating Views that Access the Database</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video12\" routerLinkActive=\"active\">Setting Up a Django Template</a>\n\n                </li>\n\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video13\" routerLinkActive=\"active\">Managing Error Messages Such as Page Not Found Error 404</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video14\" routerLinkActive=\"active\">Using Django API to Access Foreign Keys in Database Within a Template</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video15\" routerLinkActive=\"active\">Removing hardcoded URLs and namespacing URLs</a>\n\n                </li>\n\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video16\" routerLinkActive=\"active\">Creating Forms in Templates</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video17\" routerLinkActive=\"active\">Submitting and Displaying Form Results</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video18\" routerLinkActive=\"active\">Using Generic Views to Display Django Webpages</a>\n\n                </li>\n                <li class=\"collection-item avatar\">\n                  <i class=\"material-icons circle red\">play_arrow</i>\n\n                  <a routerLink=\"./video19\" routerLinkActive=\"active\">Adding CSS, Cascading Stylesheets, to Django Templates</a>\n\n                </li>\n            </ul>\n          </div>\n        </div>\n    </div>\n  </div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/course/course.component.ts":
/*!********************************************!*\
  !*** ./src/app/course/course.component.ts ***!
  \********************************************/
/*! exports provided: CourseComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CourseComponent", function() { return CourseComponent; });
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _course_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./course.service */ "./src/app/course/course.service.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../data.service */ "./src/app/data.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var angular2_materialize__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! angular2-materialize */ "./node_modules/angular2-materialize/dist/index.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};






var CourseComponent = /** @class */ (function () {
    function CourseComponent(dataservice, http, courseService, route) {
        this.dataservice = dataservice;
        this.http = http;
        this.courseService = courseService;
        this.route = route;
        this.users = [];
        this.topics = [];
        this.options = {};
        this.dataservice.username = sessionStorage.getItem('username');
        this.dataservice.id = sessionStorage.getItem('id');
        this.dataservice.authOptions = {
            headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpHeaders"]({ 'Content-Type': 'application/json', 'Authorization': 'JWT ' + sessionStorage.getItem('token') })
        };
    }
    CourseComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.dataservice.djangostudents().subscribe(function (data) {
            _this.users = data;
            console.log(data);
        });
        this.topics = this.courseService.getTopics();
        var id = +this.route.snapshot.params['id'];
        this.topic = this.courseService.getSingleTopic(id);
        this.route.params.subscribe(function (params) {
            _this.topic = _this.courseService.getSingleTopic(+params[id]);
        });
    };
    CourseComponent.prototype.logout = function () {
        this.dataservice.logout();
    };
    CourseComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["Component"])({
            selector: 'app-course',
            template: __webpack_require__(/*! ./course.component.html */ "./src/app/course/course.component.html"),
            styles: [__webpack_require__(/*! ./course.component.css */ "./src/app/course/course.component.css")],
            providers: [angular2_materialize__WEBPACK_IMPORTED_MODULE_5__["MaterializeModule"], _course_service__WEBPACK_IMPORTED_MODULE_1__["CourseService"]],
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_3__["DataService"],
            _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClient"],
            _course_service__WEBPACK_IMPORTED_MODULE_1__["CourseService"],
            _angular_router__WEBPACK_IMPORTED_MODULE_0__["ActivatedRoute"]])
    ], CourseComponent);
    return CourseComponent;
}());



/***/ }),

/***/ "./src/app/course/course.service.ts":
/*!******************************************!*\
  !*** ./src/app/course/course.service.ts ***!
  \******************************************/
/*! exports provided: CourseService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "CourseService", function() { return CourseService; });
/* harmony import */ var _topic_model__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./topic.model */ "./src/app/course/topic.model.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};


var CourseService = /** @class */ (function () {
    function CourseService() {
        this.topics = [
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](1, 'Django Definition and Installation', '/src/assets/videos/connect_sqlite.mp4'),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](2, 'Creating Your First Django Project and Your First Django Application', '/assets/videos/connect_sqlite.mp4'),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](3, 'Connecting With SQLlite, the Default Django Database System', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](4, 'Connecting Your Django Application to MySQL Database', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](5, 'Setting Up Django Administrator', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](6, 'Making Your Django Apps Reusable for Other Projects', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](7, 'Creating DJango Views', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](8, 'Using Django to Access and Manipulate Data in the Database', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](9, 'More on Using Django API to Edit Data in Database', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](10, 'Creating Django Views that Accept Arguments', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](11, 'Creating Views that Access the Database', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](12, 'Setting Up a Django Template', ''),
            // new Topic (13, 'Working with Django Models', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](14, 'Managing Error Messages Such as Page Not Found Error 404', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](15, 'Using Django API to Access Foreign Keys in Database Within a Template', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](16, 'Removing hardcoded URLs and namespacing URLs', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](17, 'Creating Forms in Templates', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](18, 'Submitting and Displaying Form Results', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](19, 'Using Generic Views to Display Django Webpages', ''),
            new _topic_model__WEBPACK_IMPORTED_MODULE_0__["Topic"](20, 'Adding CSS, Cascading Stylesheets, to Django Templates', '')
        ];
    }
    CourseService.prototype.getTopics = function () {
        return this.topics.slice();
    };
    // getSingleTopic(index: number) {
    //   return this.topics[index];
    //   }
    CourseService.prototype.getSingleTopic = function (id) {
        var topic = this.topics.find(function (data) {
            return data.id === id;
        });
        return topic;
    };
    CourseService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
            providedIn: 'root'
        })
    ], CourseService);
    return CourseService;
}());



/***/ }),

/***/ "./src/app/course/labs/labs.component.css":
/*!************************************************!*\
  !*** ./src/app/course/labs/labs.component.css ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/labs/labs.component.html":
/*!*************************************************!*\
  !*** ./src/app/course/labs/labs.component.html ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<h5 style=\"text-align:center; font-weight: bolder;\">Labs</h5>\n<div class=\"lab_area\" style=\"overflow: auto; height:450px;\">\n    <h5 class=\"course_topic\">Topic</h5>\n    <p>\n      Lorem ipsum dolor sit amet consectetur adipisicing elit. At corrupti fuga minima, veritatis saepe quaerat impedit ducimus magnam, rerum tempora non odit voluptatem ipsa pariatur fugiat! Quas consectetur error similique?\n      Lorem ipsum dolor sit amet consectetur adipisicing elit. Rem sunt id sed eligendi, delectus, unde perferendis quas, aperiam fugiat quae iusto similique officia facere voluptas quibusdam cum dignissimos nemo voluptatum.\n      Lorem ipsum dolor sit amet consectetur adipisicing elit. Iure, illo! Aliquid quae quidem tenetur natus obcaecati quisquam, dolor optio dolores eveniet ratione earum veritatis perferendis. Necessitatibus hic quasi laborum ea.\n      Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto obcaecati voluptate molestias consequuntur hic similique. Quisquam fuga facilis porro cum sint minus pariatur reprehenderit nemo, fugiat laborum nostrum earum saepe?\n      Lorem ipsum dolor sit amet consectetur adipisicing elit. Sit ab aliquam eum placeat? Architecto quos repudiandae ad ab tempore beatae nobis praesentium quas quia! Dignissimos deleniti voluptatem et quam corrupti.\n      Lorem ipsum dolor sit amet consectetur adipisicing elit. Repellendus sequi, ipsa facilis voluptas sint odit repellat officia qui praesentium quis dolores deleniti ea, ipsam, culpa doloribus incidunt. Veniam, recusandae explicabo.\n      Lorem ipsum dolor sit amet consectetur adipisicing elit. Iste odio ut voluptate perferendis ullam eaque dicta necessitatibus repellat sapiente dolorum pariatur repudiandae ratione expedita, eos reiciendis error excepturi aspernatur? Libero.\n    </p>\n  </div>\n\n"

/***/ }),

/***/ "./src/app/course/labs/labs.component.ts":
/*!***********************************************!*\
  !*** ./src/app/course/labs/labs.component.ts ***!
  \***********************************************/
/*! exports provided: LabsComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LabsComponent", function() { return LabsComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var LabsComponent = /** @class */ (function () {
    function LabsComponent() {
    }
    LabsComponent.prototype.ngOnInit = function () {
    };
    LabsComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-labs',
            template: __webpack_require__(/*! ./labs.component.html */ "./src/app/course/labs/labs.component.html"),
            styles: [__webpack_require__(/*! ./labs.component.css */ "./src/app/course/labs/labs.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], LabsComponent);
    return LabsComponent;
}());



/***/ }),

/***/ "./src/app/course/private-chat/private-chat.component.css":
/*!****************************************************************!*\
  !*** ./src/app/course/private-chat/private-chat.component.css ***!
  \****************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "#message_box {\r\n  display: block!important;\r\n  height:1.7rem!important;\r\n  padding: .5rem!important;\r\n  border: 2px solid #636566de;\r\n  transition: all 1s;\r\n  border-radius: .5rem!important;\r\n  box-shadow: none;\r\n  width: 98%!important;\r\n}\r\n\r\n\r\n#submit {\r\n  height: 2.9rem!important;\r\n  border-top-right-radius: .5rem;\r\n  border-bottom-right-radius: .5rem;\r\n  -webkit-appearance: none;\r\n     -moz-appearance: none;\r\n          appearance: none;\r\n  margin-left: -50px;\r\n  padding-right: 10px;\r\n  border-right: 2px solid #636566de;\r\n  border-top: 2px solid #636566de;\r\n  border-bottom: 2px solid #636566de;\r\n  box-shadow: none;\r\n  padding-right: 10px;\r\n  padding-left: auto;\r\n  margin-bottom: 0px;\r\n}\r\n\r\n\r\n#send_icon {\r\n  margin-left: -10px;\r\n}\r\n"

/***/ }),

/***/ "./src/app/course/private-chat/private-chat.component.html":
/*!*****************************************************************!*\
  !*** ./src/app/course/private-chat/private-chat.component.html ***!
  \*****************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n <!-- Chat View -->\n <div class=\"card medium\" style=\"max-height: 500px;\">\n  <div class=\"card-content\" style=\"overflow:auto\" id=\"chat_div_space\">\n\n    <ul>\n      <li *ngFor=\"let message of messages\" [innerText]=\"message\"><br></li>\n  </ul>\n  </div>\n</div>\n\n\n <div class=\"form-group\" style=\"display:flex\">\n  <input (keyup.enter)=\"sendMessage(chat_text)\" class=\"form-control\" type=\"text\" id=\"message_box\" name=\"chat_text\" [(ngModel)]=\"chat_text\" placeholder=\"Type Your Message Here\">\n  <button class=\"btn btn-default send\" (click)=\"sendMessage(chat_text)\" id=\"submit\">\n    <i class=\"material-icons right\" id=\"send_icon\">send</i>\n  </button>\n</div>\n\n"

/***/ }),

/***/ "./src/app/course/private-chat/private-chat.component.ts":
/*!***************************************************************!*\
  !*** ./src/app/course/private-chat/private-chat.component.ts ***!
  \***************************************************************/
/*! exports provided: PrivateChatComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PrivateChatComponent", function() { return PrivateChatComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../data.service */ "./src/app/data.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var PrivateChatComponent = /** @class */ (function () {
    function PrivateChatComponent(dataservice, http) {
        var _this = this;
        this.dataservice = dataservice;
        this.http = http;
        this.URL = '54.244.162.68:8001';
        this.users = [];
        this.chat_text = '';
        this.messages = [];
        this.dataservice.username = sessionStorage.getItem('username');
        this.websocket = new WebSocket('ws://' + '54.244.162.68:8001');
        this.websocket.onopen = function (evt) {
            _this.websocket.send(JSON.stringify({ 'user': _this.dataservice.username, 'message': '!join room' + _this.dataservice.id }));
        };
        this.websocket.onmessage = function (evt) {
            var data = JSON.parse(evt.data);
            if (data['messages'] !== undefined) {
                _this.messages = [];
                for (var i = 0; i < data['messages']['length']; i++) {
                    _this.messages.push(data['messages'][i]['user'] + ': ' + data['messages'][i]['message']);
                }
            }
            else {
                _this.messages.push(data['user'] + ': ' + data['message']);
            }
            var chat_scroll = document.getElementById('chat_div_space');
            chat_scroll.scrollTop = chat_scroll.scrollHeight;
            console.log(_this.messages);
        };
    }
    PrivateChatComponent.prototype.ngOnInit = function () {
    };
    PrivateChatComponent.prototype.sendMessage = function (message) {
        this.websocket.send(JSON.stringify({ 'user': this.dataservice.username, 'message': this.chat_text }));
        this.chat_text = '';
    };
    PrivateChatComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-private-chat',
            template: __webpack_require__(/*! ./private-chat.component.html */ "./src/app/course/private-chat/private-chat.component.html"),
            styles: [__webpack_require__(/*! ./private-chat.component.css */ "./src/app/course/private-chat/private-chat.component.css")]
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"], _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"]])
    ], PrivateChatComponent);
    return PrivateChatComponent;
}());



/***/ }),

/***/ "./src/app/course/topic-chat.component.css":
/*!*************************************************!*\
  !*** ./src/app/course/topic-chat.component.css ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "#message_box {\r\n    display: block!important;\r\n    height:1.7rem!important;\r\n    padding: .5rem!important;\r\n    border: 2px solid #636566de;\r\n    transition: all 1s;\r\n    border-radius: .5rem!important;\r\n    box-shadow: none;\r\n    width: 98%!important;\r\n  }\r\n\r\n\r\n#submit {\r\n    height: 2.9rem!important;\r\n    border-top-right-radius: .5rem;\r\n    border-bottom-right-radius: .5rem;\r\n    -webkit-appearance: none;\r\n       -moz-appearance: none;\r\n            appearance: none;\r\n    margin-left: -50px;\r\n    padding-right: 10px;\r\n    border-right: 2px solid #636566de;\r\n    border-top: 2px solid #636566de;\r\n    border-bottom: 2px solid #636566de;\r\n    box-shadow: none;\r\n    padding-right: 10px;\r\n    padding-left: auto;\r\n    margin-bottom: 0px;\r\n}\r\n\r\n\r\n#send_icon {\r\n    margin-left: -10px;\r\n}"

/***/ }),

/***/ "./src/app/course/topic-chat.component.html":
/*!**************************************************!*\
  !*** ./src/app/course/topic-chat.component.html ***!
  \**************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n <!-- Chat View -->\n <div class=\"card medium\" style=\"max-height: 500px;\">\n  <div class=\"card-content\" style=\"overflow:auto\" id=\"chat_div_space\">\n\n    <ul>\n      <li *ngFor=\"let message of messages\" [innerText]=\"message\"></li><br>\n  </ul>\n  </div>\n</div>\n\n\n <div class=\"form-group\" style=\"display:flex\">\n  <input (keyup.enter)=\"sendMessage(chat_text)\" class=\"form-control\" type=\"text\" id=\"message_box\" name=\"chat_text\" [(ngModel)]=\"chat_text\" placeholder=\"Type Your Message Here\">\n  <button class=\"btn btn-default send\" (click)=\"sendMessage(chat_text)\" id=\"submit\">\n    <i class=\"material-icons right\" id=\"send_icon\">send</i>\n  </button>\n</div>\n"

/***/ }),

/***/ "./src/app/course/topic-chat.component.ts":
/*!************************************************!*\
  !*** ./src/app/course/topic-chat.component.ts ***!
  \************************************************/
/*! exports provided: TopicChatComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TopicChatComponent", function() { return TopicChatComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../data.service */ "./src/app/data.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var TopicChatComponent = /** @class */ (function () {
    function TopicChatComponent(dataservice, http) {
        var _this = this;
        this.dataservice = dataservice;
        this.http = http;
        this.URL = '54.244.162.68:8001';
        this.users = [];
        this.images = [];
        this.selectedFile = null;
        this.chat_text = '';
        this.messages = [];
        this.onFileSelected = function (event) {
            _this.selectedFile = event.target.files[0];
            // console.log(event);
        };
        this.dataservice.username = sessionStorage.getItem('username');
        this.websocket = new WebSocket('ws://' + '54.244.162.68:8001');
        this.websocket.onopen = function (evt) {
            _this.websocket.send(JSON.stringify({ 'user': _this.dataservice.username, 'message': '!join DjangoClass' }));
        };
        this.websocket.onmessage = function (evt) {
            var data = JSON.parse(evt.data);
            if (data['messages'] !== undefined) {
                _this.messages = [];
                for (var i = 0; i < data['messages']['length']; i++) {
                    _this.messages.push(data['messages'][i]['user'] + ': ' + data['messages'][i]['message']);
                }
            }
            else {
                _this.messages.push(data['user'] + ': ' + data['message']);
            }
            var chat_scroll = document.getElementById('chat_div_space');
            chat_scroll.scrollTop = chat_scroll.scrollHeight;
            console.log(_this.messages);
        };
    }
    TopicChatComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.dataservice.djangostudents().subscribe(function (data) {
            _this.users = data;
        });
    };
    TopicChatComponent.prototype.allUsers = function () {
        var _this = this;
        this.dataservice.djangostudents().subscribe(function (data) {
            _this.users = data;
        });
    };
    TopicChatComponent.prototype.sendMessage = function (message) {
        this.websocket.send(JSON.stringify({ 'user': this.dataservice.username, 'message': this.chat_text }));
        this.chat_text = '';
    };
    TopicChatComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-topic-chat',
            template: __webpack_require__(/*! ./topic-chat.component.html */ "./src/app/course/topic-chat.component.html"),
            styles: [__webpack_require__(/*! ./topic-chat.component.css */ "./src/app/course/topic-chat.component.css")]
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"], _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"]])
    ], TopicChatComponent);
    return TopicChatComponent;
}());



/***/ }),

/***/ "./src/app/course/topic-detail/topic-detail.component.css":
/*!****************************************************************!*\
  !*** ./src/app/course/topic-detail/topic-detail.component.css ***!
  \****************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/topic-detail/topic-detail.component.html":
/*!*****************************************************************!*\
  !*** ./src/app/course/topic-detail/topic-detail.component.html ***!
  \*****************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div>\n  <div class=\"\">\n    <h6  style=\"text-align: center\">{{ topic.title }}</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/connect_sqlite.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/course/topic-detail/topic-detail.component.ts":
/*!***************************************************************!*\
  !*** ./src/app/course/topic-detail/topic-detail.component.ts ***!
  \***************************************************************/
/*! exports provided: TopicDetailComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TopicDetailComponent", function() { return TopicDetailComponent; });
/* harmony import */ var _course_service__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./../course.service */ "./src/app/course/course.service.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var TopicDetailComponent = /** @class */ (function () {
    // id: number;
    // title: string;
    // videoPath: string;
    function TopicDetailComponent(route, courseService) {
        this.route = route;
        this.courseService = courseService;
    }
    TopicDetailComponent.prototype.ngOnInit = function () {
        var _this = this;
        var id = +this.route.snapshot.params['id'];
        this.topic = this.courseService.getSingleTopic(id);
        this.route.params.subscribe(function (params) {
            _this.topic = _this.courseService.getSingleTopic(+params[id]);
        });
    };
    TopicDetailComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
            selector: 'app-topic-detail',
            template: __webpack_require__(/*! ./topic-detail.component.html */ "./src/app/course/topic-detail/topic-detail.component.html"),
            styles: [__webpack_require__(/*! ./topic-detail.component.css */ "./src/app/course/topic-detail/topic-detail.component.css")]
        }),
        __metadata("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_2__["ActivatedRoute"], _course_service__WEBPACK_IMPORTED_MODULE_0__["CourseService"]])
    ], TopicDetailComponent);
    return TopicDetailComponent;
}());



/***/ }),

/***/ "./src/app/course/topic.model.ts":
/*!***************************************!*\
  !*** ./src/app/course/topic.model.ts ***!
  \***************************************/
/*! exports provided: Topic */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Topic", function() { return Topic; });
var Topic = /** @class */ (function () {
    function Topic(id, title, videoPath) {
        this.id = id;
        this.title = title;
        this.videoPath = videoPath;
    }
    return Topic;
}());



/***/ }),

/***/ "./src/app/course/video10/video10.component.html":
/*!*******************************************************!*\
  !*** ./src/app/course/video10/video10.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Creating Django Views that Accept Arguments</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/Creating_VIEWS_that_Accept__Arguments.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/course/video10/video10.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/course/video10/video10.component.ts ***!
  \*****************************************************/
/*! exports provided: Video10Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video10Component", function() { return Video10Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video10Component = /** @class */ (function () {
    function Video10Component() {
    }
    Video10Component.prototype.ngOnInit = function () {
    };
    Video10Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video10',
            template: __webpack_require__(/*! ./video10.component.html */ "./src/app/course/video10/video10.component.html"),
        }),
        __metadata("design:paramtypes", [])
    ], Video10Component);
    return Video10Component;
}());



/***/ }),

/***/ "./src/app/course/video11/video11.component.css":
/*!******************************************************!*\
  !*** ./src/app/course/video11/video11.component.css ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/video11/video11.component.html":
/*!*******************************************************!*\
  !*** ./src/app/course/video11/video11.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Creating Views that access the Database</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/making__views_that_access_the_database.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video11/video11.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/course/video11/video11.component.ts ***!
  \*****************************************************/
/*! exports provided: Video11Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video11Component", function() { return Video11Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video11Component = /** @class */ (function () {
    function Video11Component() {
    }
    Video11Component.prototype.ngOnInit = function () {
    };
    Video11Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video11',
            template: __webpack_require__(/*! ./video11.component.html */ "./src/app/course/video11/video11.component.html"),
            styles: [__webpack_require__(/*! ./video11.component.css */ "./src/app/course/video11/video11.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], Video11Component);
    return Video11Component;
}());



/***/ }),

/***/ "./src/app/course/video12/video12.component.css":
/*!******************************************************!*\
  !*** ./src/app/course/video12/video12.component.css ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/video12/video12.component.html":
/*!*******************************************************!*\
  !*** ./src/app/course/video12/video12.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Setting Up a Django Template</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/setting_up_a_djanGo__template.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/course/video12/video12.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/course/video12/video12.component.ts ***!
  \*****************************************************/
/*! exports provided: Video12Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video12Component", function() { return Video12Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video12Component = /** @class */ (function () {
    function Video12Component() {
    }
    Video12Component.prototype.ngOnInit = function () {
    };
    Video12Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video12',
            template: __webpack_require__(/*! ./video12.component.html */ "./src/app/course/video12/video12.component.html"),
            styles: [__webpack_require__(/*! ./video12.component.css */ "./src/app/course/video12/video12.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], Video12Component);
    return Video12Component;
}());



/***/ }),

/***/ "./src/app/course/video13/video13.component.css":
/*!******************************************************!*\
  !*** ./src/app/course/video13/video13.component.css ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/video13/video13.component.html":
/*!*******************************************************!*\
  !*** ./src/app/course/video13/video13.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Managing Error Messages such as page not found</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/Managing_ErrorMessages_such_AS_pageNOTfound_Error_404.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video13/video13.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/course/video13/video13.component.ts ***!
  \*****************************************************/
/*! exports provided: Video13Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video13Component", function() { return Video13Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video13Component = /** @class */ (function () {
    function Video13Component() {
    }
    Video13Component.prototype.ngOnInit = function () {
    };
    Video13Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video13',
            template: __webpack_require__(/*! ./video13.component.html */ "./src/app/course/video13/video13.component.html"),
            styles: [__webpack_require__(/*! ./video13.component.css */ "./src/app/course/video13/video13.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], Video13Component);
    return Video13Component;
}());



/***/ }),

/***/ "./src/app/course/video14/video14.component.css":
/*!******************************************************!*\
  !*** ./src/app/course/video14/video14.component.css ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/video14/video14.component.html":
/*!*******************************************************!*\
  !*** ./src/app/course/video14/video14.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Using Django API to Access Foreign eys in Database within a template</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/Using_DJango_API_to_ACCess_Foreign_keys_in_Database_Within_a_template.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video14/video14.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/course/video14/video14.component.ts ***!
  \*****************************************************/
/*! exports provided: Video14Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video14Component", function() { return Video14Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video14Component = /** @class */ (function () {
    function Video14Component() {
    }
    Video14Component.prototype.ngOnInit = function () {
    };
    Video14Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video14',
            template: __webpack_require__(/*! ./video14.component.html */ "./src/app/course/video14/video14.component.html"),
            styles: [__webpack_require__(/*! ./video14.component.css */ "./src/app/course/video14/video14.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], Video14Component);
    return Video14Component;
}());



/***/ }),

/***/ "./src/app/course/video15/video15.component.css":
/*!******************************************************!*\
  !*** ./src/app/course/video15/video15.component.css ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/video15/video15.component.html":
/*!*******************************************************!*\
  !*** ./src/app/course/video15/video15.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Removing Hardcoded URLs and namespacing URLs</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/Replacing_hardcoded_urls_WITH__Dynamic_values_namespacing_urls.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video15/video15.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/course/video15/video15.component.ts ***!
  \*****************************************************/
/*! exports provided: Video15Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video15Component", function() { return Video15Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video15Component = /** @class */ (function () {
    function Video15Component() {
    }
    Video15Component.prototype.ngOnInit = function () {
    };
    Video15Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video15',
            template: __webpack_require__(/*! ./video15.component.html */ "./src/app/course/video15/video15.component.html"),
            styles: [__webpack_require__(/*! ./video15.component.css */ "./src/app/course/video15/video15.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], Video15Component);
    return Video15Component;
}());



/***/ }),

/***/ "./src/app/course/video16/video16.component.css":
/*!******************************************************!*\
  !*** ./src/app/course/video16/video16.component.css ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/video16/video16.component.html":
/*!*******************************************************!*\
  !*** ./src/app/course/video16/video16.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Creating Forms in Templates</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/creating_FORMS_in_teMplates.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/course/video16/video16.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/course/video16/video16.component.ts ***!
  \*****************************************************/
/*! exports provided: Video16Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video16Component", function() { return Video16Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video16Component = /** @class */ (function () {
    function Video16Component() {
    }
    Video16Component.prototype.ngOnInit = function () {
    };
    Video16Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video16',
            template: __webpack_require__(/*! ./video16.component.html */ "./src/app/course/video16/video16.component.html"),
            styles: [__webpack_require__(/*! ./video16.component.css */ "./src/app/course/video16/video16.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], Video16Component);
    return Video16Component;
}());



/***/ }),

/***/ "./src/app/course/video17/video17.component.css":
/*!******************************************************!*\
  !*** ./src/app/course/video17/video17.component.css ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/video17/video17.component.html":
/*!*******************************************************!*\
  !*** ./src/app/course/video17/video17.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Submitting and Displaying form Results</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/Submitting_Form__and_displaying_results.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video17/video17.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/course/video17/video17.component.ts ***!
  \*****************************************************/
/*! exports provided: Video17Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video17Component", function() { return Video17Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video17Component = /** @class */ (function () {
    function Video17Component() {
    }
    Video17Component.prototype.ngOnInit = function () {
    };
    Video17Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video17',
            template: __webpack_require__(/*! ./video17.component.html */ "./src/app/course/video17/video17.component.html"),
            styles: [__webpack_require__(/*! ./video17.component.css */ "./src/app/course/video17/video17.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], Video17Component);
    return Video17Component;
}());



/***/ }),

/***/ "./src/app/course/video18/video18.component.css":
/*!******************************************************!*\
  !*** ./src/app/course/video18/video18.component.css ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/video18/video18.component.html":
/*!*******************************************************!*\
  !*** ./src/app/course/video18/video18.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Using Generic Views to Display Django Web pages</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/Django_genericview_.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video18/video18.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/course/video18/video18.component.ts ***!
  \*****************************************************/
/*! exports provided: Video18Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video18Component", function() { return Video18Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video18Component = /** @class */ (function () {
    function Video18Component() {
    }
    Video18Component.prototype.ngOnInit = function () {
    };
    Video18Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video18',
            template: __webpack_require__(/*! ./video18.component.html */ "./src/app/course/video18/video18.component.html"),
            styles: [__webpack_require__(/*! ./video18.component.css */ "./src/app/course/video18/video18.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], Video18Component);
    return Video18Component;
}());



/***/ }),

/***/ "./src/app/course/video19/video19.component.css":
/*!******************************************************!*\
  !*** ./src/app/course/video19/video19.component.css ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/video19/video19.component.html":
/*!*******************************************************!*\
  !*** ./src/app/course/video19/video19.component.html ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Adding CSS to Django Templates</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/Adding_cascading_stylesheets_CSS_to_Django_templates.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video19/video19.component.ts":
/*!*****************************************************!*\
  !*** ./src/app/course/video19/video19.component.ts ***!
  \*****************************************************/
/*! exports provided: Video19Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video19Component", function() { return Video19Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video19Component = /** @class */ (function () {
    function Video19Component() {
    }
    Video19Component.prototype.ngOnInit = function () {
    };
    Video19Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video19',
            template: __webpack_require__(/*! ./video19.component.html */ "./src/app/course/video19/video19.component.html"),
            styles: [__webpack_require__(/*! ./video19.component.css */ "./src/app/course/video19/video19.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], Video19Component);
    return Video19Component;
}());



/***/ }),

/***/ "./src/app/course/video2/video2.component.html":
/*!*****************************************************!*\
  !*** ./src/app/course/video2/video2.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Creating Your First Django Project and Your First Django Application</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/connect_sqlite.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video2/video2.component.ts":
/*!***************************************************!*\
  !*** ./src/app/course/video2/video2.component.ts ***!
  \***************************************************/
/*! exports provided: Video2Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video2Component", function() { return Video2Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video2Component = /** @class */ (function () {
    function Video2Component() {
    }
    Video2Component.prototype.ngOnInit = function () {
    };
    Video2Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video2',
            template: __webpack_require__(/*! ./video2.component.html */ "./src/app/course/video2/video2.component.html"),
        }),
        __metadata("design:paramtypes", [])
    ], Video2Component);
    return Video2Component;
}());



/***/ }),

/***/ "./src/app/course/video3/video3.component.html":
/*!*****************************************************!*\
  !*** ./src/app/course/video3/video3.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Connecting With SQLlite, the Default Django Database System</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/connect_sqlite.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video3/video3.component.ts":
/*!***************************************************!*\
  !*** ./src/app/course/video3/video3.component.ts ***!
  \***************************************************/
/*! exports provided: Video3Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video3Component", function() { return Video3Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video3Component = /** @class */ (function () {
    function Video3Component() {
    }
    Video3Component.prototype.ngOnInit = function () {
    };
    Video3Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video3',
            template: __webpack_require__(/*! ./video3.component.html */ "./src/app/course/video3/video3.component.html"),
        }),
        __metadata("design:paramtypes", [])
    ], Video3Component);
    return Video3Component;
}());



/***/ }),

/***/ "./src/app/course/video4/video4.component.html":
/*!*****************************************************!*\
  !*** ./src/app/course/video4/video4.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Connecting Your Django Application to MySQL Database</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/connect_sqlite.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video4/video4.component.ts":
/*!***************************************************!*\
  !*** ./src/app/course/video4/video4.component.ts ***!
  \***************************************************/
/*! exports provided: Video4Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video4Component", function() { return Video4Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video4Component = /** @class */ (function () {
    function Video4Component() {
    }
    Video4Component.prototype.ngOnInit = function () {
    };
    Video4Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video4',
            template: __webpack_require__(/*! ./video4.component.html */ "./src/app/course/video4/video4.component.html"),
        }),
        __metadata("design:paramtypes", [])
    ], Video4Component);
    return Video4Component;
}());



/***/ }),

/***/ "./src/app/course/video5/video5.component.html":
/*!*****************************************************!*\
  !*** ./src/app/course/video5/video5.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Setting Up Django Administrator</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/connect_sqlite.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video5/video5.component.ts":
/*!***************************************************!*\
  !*** ./src/app/course/video5/video5.component.ts ***!
  \***************************************************/
/*! exports provided: Video5Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video5Component", function() { return Video5Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video5Component = /** @class */ (function () {
    function Video5Component() {
    }
    Video5Component.prototype.ngOnInit = function () {
    };
    Video5Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video5',
            template: __webpack_require__(/*! ./video5.component.html */ "./src/app/course/video5/video5.component.html"),
        }),
        __metadata("design:paramtypes", [])
    ], Video5Component);
    return Video5Component;
}());



/***/ }),

/***/ "./src/app/course/video6/video6.component.html":
/*!*****************************************************!*\
  !*** ./src/app/course/video6/video6.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Making Your Django Apps Reusable for Other Projects</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/makingAppsReusable.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/course/video6/video6.component.ts":
/*!***************************************************!*\
  !*** ./src/app/course/video6/video6.component.ts ***!
  \***************************************************/
/*! exports provided: Video6Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video6Component", function() { return Video6Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video6Component = /** @class */ (function () {
    function Video6Component() {
    }
    Video6Component.prototype.ngOnInit = function () {
    };
    Video6Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video6',
            template: __webpack_require__(/*! ./video6.component.html */ "./src/app/course/video6/video6.component.html"),
        }),
        __metadata("design:paramtypes", [])
    ], Video6Component);
    return Video6Component;
}());



/***/ }),

/***/ "./src/app/course/video7/video7.component.html":
/*!*****************************************************!*\
  !*** ./src/app/course/video7/video7.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n <div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Creating DJango Views</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/create_django_view.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video7/video7.component.ts":
/*!***************************************************!*\
  !*** ./src/app/course/video7/video7.component.ts ***!
  \***************************************************/
/*! exports provided: Video7Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video7Component", function() { return Video7Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video7Component = /** @class */ (function () {
    function Video7Component() {
    }
    Video7Component.prototype.ngOnInit = function () {
    };
    Video7Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video7',
            template: __webpack_require__(/*! ./video7.component.html */ "./src/app/course/video7/video7.component.html"),
        }),
        __metadata("design:paramtypes", [])
    ], Video7Component);
    return Video7Component;
}());



/***/ }),

/***/ "./src/app/course/video8/video8.component.html":
/*!*****************************************************!*\
  !*** ./src/app/course/video8/video8.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Using Django to Access and Manipulate Data in the Database</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/Using_Django_API_to_ACCess_n_maniPulate_the_data_in_database.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/course/video8/video8.component.ts":
/*!***************************************************!*\
  !*** ./src/app/course/video8/video8.component.ts ***!
  \***************************************************/
/*! exports provided: Video8Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video8Component", function() { return Video8Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video8Component = /** @class */ (function () {
    function Video8Component() {
    }
    Video8Component.prototype.ngOnInit = function () {
    };
    Video8Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video8',
            template: __webpack_require__(/*! ./video8.component.html */ "./src/app/course/video8/video8.component.html"),
        }),
        __metadata("design:paramtypes", [])
    ], Video8Component);
    return Video8Component;
}());



/***/ }),

/***/ "./src/app/course/video9/video9.component.html":
/*!*****************************************************!*\
  !*** ./src/app/course/video9/video9.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div>\n  <div class=\"\">\n    <h6 style=\"text-align: center\">Working with Django Models</h6>\n    <mat-video  [preload]=\"true\" [download]=\"false\">\n\n      <source src=\"/assets/videos/more_on_Using_DJango_API_to_edit_datA_in_databasE.mp4\" type=\"video/mp4\">\n    </mat-video>\n  </div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/course/video9/video9.component.ts":
/*!***************************************************!*\
  !*** ./src/app/course/video9/video9.component.ts ***!
  \***************************************************/
/*! exports provided: Video9Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Video9Component", function() { return Video9Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var Video9Component = /** @class */ (function () {
    function Video9Component() {
    }
    Video9Component.prototype.ngOnInit = function () {
    };
    Video9Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-video9',
            template: __webpack_require__(/*! ./video9.component.html */ "./src/app/course/video9/video9.component.html"),
        }),
        __metadata("design:paramtypes", [])
    ], Video9Component);
    return Video9Component;
}());



/***/ }),

/***/ "./src/app/course/videos/videos.component.css":
/*!****************************************************!*\
  !*** ./src/app/course/videos/videos.component.css ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ""

/***/ }),

/***/ "./src/app/course/videos/videos.component.html":
/*!*****************************************************!*\
  !*** ./src/app/course/videos/videos.component.html ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n\n    <div>\n\n        <div class=\"\">\n          <h6 style=\"text-align: center\">Django Definition and Installation</h6>\n          <mat-video title=\"\">\n\n            <source src=\"/src/assets/videos/connect_sqlite.mp4\" type=\"video/mp4\">\n          </mat-video>\n        </div>\n    </div>\n\n\n\n\n"

/***/ }),

/***/ "./src/app/course/videos/videos.component.ts":
/*!***************************************************!*\
  !*** ./src/app/course/videos/videos.component.ts ***!
  \***************************************************/
/*! exports provided: VideosComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VideosComponent", function() { return VideosComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var VideosComponent = /** @class */ (function () {
    function VideosComponent() {
    }
    VideosComponent.prototype.ngOnInit = function () {
    };
    VideosComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-videos',
            template: __webpack_require__(/*! ./videos.component.html */ "./src/app/course/videos/videos.component.html"),
            styles: [__webpack_require__(/*! ./videos.component.css */ "./src/app/course/videos/videos.component.css")]
        }),
        __metadata("design:paramtypes", [])
    ], VideosComponent);
    return VideosComponent;
}());



/***/ }),

/***/ "./src/app/course2/course2.component.css":
/*!***********************************************!*\
  !*** ./src/app/course2/course2.component.css ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\r\n\r\nnav {\r\n  background-color: #6c63ff;\r\n}\r\n\r\nnav ul a:hover {\r\n\r\nborder-bottom: 4px solid #6c63ff;\r\n}\r\n\r\n.logo {\r\n  height: 15%;\r\n  width: 15%;\r\n  margin-top: 17px\r\n  }\r\n\r\n.logo-text {\r\nposition: absolute;\r\npadding-left: 3px;\r\nfont-weight: 700;\r\nfont-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\r\nfont-size: 1.4rem;\r\n}\r\n\r\n.dropdown {\r\nposition: absolute;\r\n}\r\n\r\n.dropdown:hover {\r\nbackground-color: #6c63ff;\r\nborder-bottom: 4px solid #6c63ff;\r\n}\r\n\r\n.dropdown-content{\r\n  width: -webkit-max-content !important;\r\n  width: -moz-max-content !important;\r\n  width: max-content !important;\r\n  height:auto !important;\r\n}\r\n\r\n#video {\r\nmargin-right: 4px;\r\nmargin-left: 4px;\r\n}\r\n\r\n#lab {\r\nmargin-right: 4px;\r\nmargin-left: 4px;\r\n}\r\n\r\n#chat {\r\n  margin-right: 4px;\r\n  margin-left: 4px;\r\n}\r\n\r\n.lab_area {\r\n  border-radius: 20px;\r\n  border: 2px solid #cdd1d4de;\r\n  height: 400px;\r\n  width: 600px;\r\n  margin-left: 10px;\r\n}\r\n\r\n.course_topic {\r\n  background-color: black;\r\n  height: 35px;\r\n  text-align: center;\r\n  color: aliceblue;\r\n  font-weight: 400;\r\n  margin-top: 0px;\r\n  border-top-right-radius: 20px;\r\n  border-top-left-radius: 20px;\r\n}\r\n\r\n#message_box {\r\n  display: block!important;\r\n  height:1.7rem!important;\r\n  padding: .5rem!important;\r\n  border: 2px solid #636566de;\r\n  transition: all 1s;\r\n  border-radius: .5rem!important;\r\n  box-shadow: none;\r\n  width: 98%!important;\r\n}\r\n\r\n#submit {\r\n  height: 2.9rem!important;\r\n  border-top-right-radius: .5rem;\r\n  border-bottom-right-radius: .5rem;\r\n  -webkit-appearance: none;\r\n     -moz-appearance: none;\r\n          appearance: none;\r\n  margin-left: -50px;\r\n  padding-right: 10px;\r\n  border-right: 2px solid #636566de;\r\n  border-top: 2px solid #636566de;\r\n  border-bottom: 2px solid #636566de;\r\n  box-shadow: none;\r\n  padding-right: 10px;\r\n  padding-left: auto;\r\n  margin-bottom: 0px;\r\n}\r\n\r\n#send_icon {\r\n  margin-left: -10px;\r\n}\r\n"

/***/ }),

/***/ "./src/app/course2/course2.component.html":
/*!************************************************!*\
  !*** ./src/app/course2/course2.component.html ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n<div class=\"navbar \">\n  <nav>\n    <div class=\"nav-wrapper\">\n      <div class=\"container-fluid\">\n        <div class=\"row\">\n\n          <div class=\"col l3 m3 s3\">\n            <a class=\"brand-logo\"><img src=\"/src/assets/image/Final-Logo.png\" alt=\"nav-logo\" class=\"logo\"><span class=\"logo-text\">ClassRoom</span></a>\n          </div>\n\n          <div class=\"col l3 m3 s3\">\n            <a materialize=\"dropdown\" class=\"dropdown-button dropdown\" data-activates=\"dropdown1\">Linux Fundamentals<i class=\"material-icons right\">arrow_drop_down</i></a>\n            <!-- Dropdown Structure -->\n            <ul id=\"dropdown1\" class=\"dropdown-content\">\n                <li><a routerLink=\"/classroom\" routerLinkActive>Django</a></li>\n                <li class=\"divider\"></li>\n                <li><a >Linux Fundamentals</a></li>\n            </ul>\n\n          </div>\n\n            <div class=\"col l6 m6 s6\">\n              <ul class=\"right\">\n                <li><a>{{dataservice.username}}</a></li>\n                <li><a (click)=\"logout()\" id=\"logout\">LOGOUT</a></li>\n              </ul>\n            </div>\n        </div>\n      </div>\n    </div>\n  </nav>\n</div>\n\n<div class=\"container-fluid\">\n  <div class=\"row\">\n    <div class=\"col l3 m3 s3\" style=\"background-color:#4d394b; height: 100%;\">\n      <h6 style=\"text-align: center; font-weight: bold;\">Registered Students | {{users.length}}</h6>\n      <div style=\"height:450px; overflow: auto;\">\n        <ul>\n          <li id=\"students\" style=\"color:darkgrey; font-weight: bolder; font-size: 15px;\"\n              *ngFor=\"let user of users\"><a> {{ user.username }} </a>\n          </li><br>\n        </ul>\n      </div>\n    </div>\n    <div class=\"col l6 m6 s9\">\n      <ul style=\"display:flex;\">\n        <li><a routerLink= \"./videos\" routerLinkActive=\"active\" id=\"video\">Video</a></li> |\n        <li><a href= \"\" target=\"_blank\" id=\"lab\">Labs</a></li> |\n        <li><a routerLink= \"./course-chat\" routerLinkActive=\"active\" id=\"chat\"> Chat</a></li>\n      </ul>\n      <hr>\n      <div style=\"max-height:600px; overflow: auto;\">\n        <router-outlet></router-outlet>\n      </div>\n    </div>\n    <div class=\"col l3 m3 s12\">\n      <div class=\"\">\n\n          <h5 style=\"text-align:center; font-weight: bolder;\">Topics</h5>\n          <div class=\"course_topic_area\" style=\"height: 450px; overflow: auto;\">\n          <ul class=\"collection\">\n\n              <li class=\"collection-item avatar\">\n                <i class=\"material-icons circle red\">play_arrow</i>\n\n                <a >Demo Topic Here</a>\n\n              </li>\n\n            </ul>\n          </div>\n        </div>\n    </div>\n  </div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/course2/course2.component.ts":
/*!**********************************************!*\
  !*** ./src/app/course2/course2.component.ts ***!
  \**********************************************/
/*! exports provided: Course2Component */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Course2Component", function() { return Course2Component; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../data.service */ "./src/app/data.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



// import { MaterializeModule } from 'angular2-materialize';
var Course2Component = /** @class */ (function () {
    function Course2Component(dataservice, http) {
        this.dataservice = dataservice;
        this.http = http;
        this.users = [];
        this.options = {};
        this.dataservice.username = sessionStorage.getItem('username');
        this.dataservice.authOptions = {
            headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpHeaders"]({ 'Content-Type': 'application/json', 'Authorization': 'JWT ' + sessionStorage.getItem('token') })
        };
    }
    Course2Component.prototype.ngOnInit = function () {
        // this.dataservice.groupclassusers().subscribe((data: Array<object>) => {
        //   this.users = data;
        //   console.log(data);
        // });
    };
    Course2Component.prototype.logout = function () {
        this.dataservice.logout();
    };
    Course2Component = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-course2',
            template: __webpack_require__(/*! ./course2.component.html */ "./src/app/course2/course2.component.html"),
            styles: [__webpack_require__(/*! ./course2.component.css */ "./src/app/course2/course2.component.css")]
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"], _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"]])
    ], Course2Component);
    return Course2Component;
}());



/***/ }),

/***/ "./src/app/data.service.ts":
/*!*********************************!*\
  !*** ./src/app/data.service.ts ***!
  \*********************************/
/*! exports provided: DataService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DataService", function() { return DataService; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var DataService = /** @class */ (function () {
    function DataService(http, router) {
        this.http = http;
        this.router = router;
        this.URL = '54.244.162.68:8001';
        this.httpOptions = {
            headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpHeaders"]({ 'Content-Type': 'application/json' })
        };
    }
    // groupclassusers() {
    //     return this.http.get('http://' + this.URL + '/api/v1/groupclass-api/groupclassusers/');
    // }
    DataService.prototype.djangostudents = function () {
        return this.http.get('http://' + this.URL + '/classroom/djangostudent-api/djangostudent/');
    };
    DataService.prototype.createUser = function () {
        var _this = this;
        this.http.post('http://' + this.URL + '/classroom/djangostudent-api/djangostudent/', JSON.stringify({ 'email': this.createuser_email, 'password': this.createuser_password, 'username': this.createuser_username }), this.httpOptions).subscribe(function (data) {
            _this.message = data['message'];
            _this.createuser_email = '';
            _this.createuser_password = '';
            _this.createuser_username = '';
            _this.id = '';
        }, function (err) {
            _this.message = 'User Creation Failed! Unexpected Error!';
            console.error(err);
            _this.createuser_email = '';
            _this.createuser_password = '';
            _this.createuser_username = '';
        });
    };
    DataService.prototype.login = function () {
        var _this = this;
        this.http.post('http://' + this.URL + '/classroom/api-token-auth/', JSON.stringify({ 'username': this.login_username, 'password': this.login_password }), this.httpOptions).subscribe(function (data) {
            sessionStorage.setItem('username', data['name']);
            sessionStorage.setItem('token', data['token']);
            localStorage.setItem('token', data['token']);
            sessionStorage.setItem('id', data['id']);
            _this.username = _this.login_username;
            _this.router.navigate(['classroom']);
            _this.login_username = '';
            _this.login_password = '';
            _this.id = '';
            console.log(_this.username);
            console.log(_this.id);
            _this.authOptions = {
                headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpHeaders"]({ 'Content-Type': 'application/json', 'Authorization': 'JWT ' + data['token'] })
            };
        }, function (err) {
            if (err['status'] === 400) {
                _this.message = 'Login Failed: Invalid Credentials.';
            }
            else {
                _this.message = 'Login Failed! Unexpected Error!';
                console.error(err);
                _this.login_username = '';
                _this.login_password = '';
            }
        });
    };
    DataService.prototype.islogin = function () {
        return !!sessionStorage.getItem('token');
    };
    DataService.prototype.logout = function () {
        this.username = '';
        this.router.navigate(['login']);
        sessionStorage.removeItem('username');
        sessionStorage.removeItem('token');
        localStorage.removeItem('token');
        sessionStorage.removeItem('id');
    };
    DataService = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Injectable"])({
            providedIn: 'root'
        }),
        __metadata("design:paramtypes", [_angular_common_http__WEBPACK_IMPORTED_MODULE_1__["HttpClient"], _angular_router__WEBPACK_IMPORTED_MODULE_2__["Router"]])
    ], DataService);
    return DataService;
}());



/***/ }),

/***/ "./src/app/home/home.component.css":
/*!*****************************************!*\
  !*** ./src/app/home/home.component.css ***!
  \*****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "nav {\r\n    background-color:#6c63ff ;\r\n    box-shadow: none;\r\n    border-bottom: 1px;\r\n    \r\n}\r\n\r\n.nav-wrapper {\r\n  padding-left: 35px;\r\n  padding-right: 30px;\r\n}\r\n\r\n.logo {\r\n  height: 15%;\r\n  width: 15%;\r\n  margin-top: 17px\r\n  }\r\n\r\n.logo-text {\r\n  position: absolute;\r\n  padding-left: 3px;\r\n  font-weight: 700;\r\n  \r\n  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\r\n  font-size: 1.7rem;\r\n  \r\n  }\r\n\r\nnav ul a:hover {\r\n  \r\n  border-bottom: 4px solid #6c63ff;\r\n}\r\n\r\nimg {\r\n  \r\n  height: 100%;\r\n  width: 150%;\r\n}\r\n\r\n/* .login_wrapper {\r\n  border: 2px solid #cdd1d4de;\r\n  border-radius: 4px;\r\n} */\r\n\r\n#login_username {\r\n    display: block!important;\r\n    height:1.82rem!important;\r\n    padding: .5rem!important;\r\n    border: 1px solid #cdd1d4de;\r\n    transition: all 1s;\r\n    border-radius: .25rem!important;\r\n    box-shadow: none;\r\n    width: 96%!important;\r\n  }\r\n\r\n#login_password {\r\n    display: block!important;\r\n    height:1.82rem!important;\r\n    padding: .5rem!important;\r\n    border: 1px solid #cdd1d4de;\r\n    transition: all 1s;\r\n    border-radius: .25rem!important;\r\n    box-shadow: none;\r\n    width: 96%!important;\r\n  }\r\n\r\n#login_project {\r\n    display: block!important;\r\n    height:1.82rem!important;\r\n    padding: .5rem!important;\r\n    border: 1px solid #cdd1d4de;\r\n    transition: all 1s;\r\n    border-radius: .25rem!important;\r\n    box-shadow: none;\r\n    width: 96%!important;\r\n  }\r\n\r\n.submit {\r\n    width:100%!important;\r\n    background-color:#6c63ff\r\n  }\r\n\r\n#home_login {\r\n      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\r\n      font-size: 1.2rem;\r\n      font-weight: bolder;\r\n      color: rgba(90, 84, 84, 0.61);\r\n  }\r\n\r\na {\r\n      text-decoration: none;\r\n  }\r\n\r\n.click {\r\n      font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;\r\n      text-align: center;\r\n      \r\n      margin-right: auto;\r\n      margin-left: auto;\r\n  }"

/***/ }),

/***/ "./src/app/home/home.component.html":
/*!******************************************!*\
  !*** ./src/app/home/home.component.html ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"navbar \">\n  <nav>\n    <div class=\"nav-wrapper\">\n      <div class=\"container-fluid\">\n          <a routerLink=\"\" routerLinkActive class=\"brand-logo\"><img src=\"/src/assets/image/Final-Logo.png\" alt=\"nav-logo\" class=\"logo\"><span class=\"logo-text\">ClassRoom</span></a>\n        <ul class=\"right hide-on-med-and-down\">\n          <li><a routerLink=\"/login\" routerLinkActive>LOGIN</a></li>\n          <li><a routerLink=\"/signup\" routerLinkActive>REGISTER</a></li>\n        </ul>\n      </div>\n    </div>\n  </nav>\n</div>\n\n<br>\n<div class=\"row\">\n\n<div class=\"container\">\n<div class=\"col m6 s12 login_section\">\n  <p>{{dataservice.message}}</p>\n  <div class=\"login_wrapper\">\n      <br><br>\n      <h4 class=\"bold center\" id=\"home_login\">LOGIN</h4>\n      <form (ngSubmit)=\"login()\">\n          <div class=\"form-group\">\n              <input required class=\"form-control\" type=\"text\" id=\"login_username\" [(ngModel)]=\"dataservice.login_username\" name=\"username\" placeholder=\"Username\">\n          </div>\n          <br>\n          <div class=\"form-group\">\n              <input required class=\"form-control\" type=\"password\" id=\"login_password\" [(ngModel)]=\"dataservice.login_password\" name=\"password\" placeholder=\"Password\">\n          </div>\n          <br>\n\n          <div class=\"form-group\">\n              <input class=\"form-control btn btn-default submit\" (click)=\"login()\" type=\"submit\" value=\"LOGIN\">\n          </div>\n      </form>\n      <br>\n\n  </div>\n</div>\n<div class=\"col m6 s12\">\n  <img src=\"/src/assets/image/programming.png\" alt=\"Banner\">\n</div>\n</div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/home/home.component.ts":
/*!****************************************!*\
  !*** ./src/app/home/home.component.ts ***!
  \****************************************/
/*! exports provided: HomeComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HomeComponent", function() { return HomeComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../data.service */ "./src/app/data.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var HomeComponent = /** @class */ (function () {
    function HomeComponent(dataservice, http) {
        this.dataservice = dataservice;
        this.http = http;
        this.users = [];
        this.chat_text = '';
        this.messages = [];
    }
    HomeComponent.prototype.ngOnInit = function () {
    };
    HomeComponent.prototype.login = function () {
        this.dataservice.login();
    };
    HomeComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-home',
            template: __webpack_require__(/*! ./home.component.html */ "./src/app/home/home.component.html"),
            styles: [__webpack_require__(/*! ./home.component.css */ "./src/app/home/home.component.css")]
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"], _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"]])
    ], HomeComponent);
    return HomeComponent;
}());



/***/ }),

/***/ "./src/app/linux/linux-chat/linux-chat.component.css":
/*!***********************************************************!*\
  !*** ./src/app/linux/linux-chat/linux-chat.component.css ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "#message_box {\r\n  display: block!important;\r\n  height:1.7rem!important;\r\n  padding: .5rem!important;\r\n  border: 2px solid #636566de;\r\n  transition: all 1s;\r\n  border-radius: .5rem!important;\r\n  box-shadow: none;\r\n  width: 98%!important;\r\n}\r\n\r\n\r\n#submit {\r\n  height: 2.9rem!important;\r\n  border-top-right-radius: .5rem;\r\n  border-bottom-right-radius: .5rem;\r\n  -webkit-appearance: none;\r\n     -moz-appearance: none;\r\n          appearance: none;\r\n  margin-left: -50px;\r\n  padding-right: 10px;\r\n  border-right: 2px solid #636566de;\r\n  border-top: 2px solid #636566de;\r\n  border-bottom: 2px solid #636566de;\r\n  box-shadow: none;\r\n  padding-right: 10px;\r\n  padding-left: auto;\r\n  margin-bottom: 0px;\r\n}\r\n\r\n\r\n#send_icon {\r\n  margin-left: -10px;\r\n}\r\n"

/***/ }),

/***/ "./src/app/linux/linux-chat/linux-chat.component.html":
/*!************************************************************!*\
  !*** ./src/app/linux/linux-chat/linux-chat.component.html ***!
  \************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n\n <!-- Chat View -->\n <div class=\"card medium\" style=\"max-height: 500px;\">\n  <div class=\"card-content\" style=\"overflow:auto\" id=\"chat_div_space\">\n\n    <ul>\n      <li *ngFor=\"let message of messages\" [innerText]=\"message\"></li><br>\n  </ul>\n  </div>\n</div>\n\n\n <div class=\"form-group\" style=\"display:flex\">\n  <input (keyup.enter)=\"sendMessage(chat_text)\" class=\"form-control\" type=\"text\" id=\"message_box\" name=\"chat_text\" [(ngModel)]=\"chat_text\" placeholder=\"Type Your Message Here\">\n  <button class=\"btn btn-default send\" (click)=\"sendMessage(chat_text)\" id=\"submit\">\n    <i class=\"material-icons right\" id=\"send_icon\">send</i>\n  </button>\n</div>\n"

/***/ }),

/***/ "./src/app/linux/linux-chat/linux-chat.component.ts":
/*!**********************************************************!*\
  !*** ./src/app/linux/linux-chat/linux-chat.component.ts ***!
  \**********************************************************/
/*! exports provided: LinuxChatComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LinuxChatComponent", function() { return LinuxChatComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../data.service */ "./src/app/data.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var LinuxChatComponent = /** @class */ (function () {
    function LinuxChatComponent(dataservice, http) {
        var _this = this;
        this.dataservice = dataservice;
        this.http = http;
        this.URL = '54.244.162.68:8001';
        this.users = [];
        this.images = [];
        this.selectedFile = null;
        this.chat_text = '';
        this.messages = [];
        this.dataservice.username = sessionStorage.getItem('username');
        this.websocket = new WebSocket('ws://' + '54.244.162.68:8001');
        this.websocket.onopen = function (evt) {
            _this.websocket.send(JSON.stringify({ 'user': _this.dataservice.username, 'message': '!join linuxroom' }));
        };
        this.websocket.onmessage = function (evt) {
            var data = JSON.parse(evt.data);
            if (data['messages'] !== undefined) {
                _this.messages = [];
                for (var i = 0; i < data['messages']['length']; i++) {
                    _this.messages.push(data['messages'][i]['user'] + ': ' + data['messages'][i]['message']);
                }
            }
            else {
                _this.messages.push(data['user'] + ': ' + data['message']);
            }
            var chat_scroll = document.getElementById('chat_div_space');
            chat_scroll.scrollTop = chat_scroll.scrollHeight;
            console.log(_this.messages);
        };
    }
    LinuxChatComponent.prototype.ngOnInit = function () {
        var _this = this;
        // this.dataservice.groupclassusers().subscribe((data: Array<object>) => {
        //   this.users = data;
        //   console.log(data);
        // });
        this.dataservice.djangostudents().subscribe(function (data) {
            _this.users = data;
        });
    };
    LinuxChatComponent.prototype.allUsers = function () {
        var _this = this;
        //   this.dataservice.groupclassusers().subscribe((data: Array<object>) => {
        //     this.users = data;
        //     console.log(data);
        // });
        this.dataservice.djangostudents().subscribe(function (data) {
            _this.users = data;
        });
    };
    LinuxChatComponent.prototype.sendMessage = function (message) {
        this.websocket.send(JSON.stringify({ 'user': this.dataservice.username, 'message': this.chat_text }));
        this.chat_text = '';
    };
    LinuxChatComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-linux-chat',
            template: __webpack_require__(/*! ./linux-chat.component.html */ "./src/app/linux/linux-chat/linux-chat.component.html"),
            styles: [__webpack_require__(/*! ./linux-chat.component.css */ "./src/app/linux/linux-chat/linux-chat.component.css")]
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"], _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"]])
    ], LinuxChatComponent);
    return LinuxChatComponent;
}());



/***/ }),

/***/ "./src/app/linux/linux-routing.module.ts":
/*!***********************************************!*\
  !*** ./src/app/linux/linux-routing.module.ts ***!
  \***********************************************/
/*! exports provided: LinuxRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LinuxRoutingModule", function() { return LinuxRoutingModule; });
/* harmony import */ var _linux_chat_linux_chat_component__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./linux-chat/linux-chat.component */ "./src/app/linux/linux-chat/linux-chat.component.ts");
/* harmony import */ var _linux_component__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./linux.component */ "./src/app/linux/linux.component.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm5/platform-browser.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _auth_guard__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../auth.guard */ "./src/app/auth.guard.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};






var linuxRoutes = [
    {
        path: 'linux',
        component: _linux_component__WEBPACK_IMPORTED_MODULE_1__["LinuxComponent"], canActivate: [_auth_guard__WEBPACK_IMPORTED_MODULE_5__["AuthGuard"]],
        children: [
            {
                path: '',
                children: [
                    { path: 'linux-chat', component: _linux_chat_linux_chat_component__WEBPACK_IMPORTED_MODULE_0__["LinuxChatComponent"] },
                ]
            }
        ]
    }
];
var LinuxRoutingModule = /** @class */ (function () {
    function LinuxRoutingModule() {
    }
    LinuxRoutingModule = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
            imports: [
                _angular_platform_browser__WEBPACK_IMPORTED_MODULE_3__["BrowserModule"],
                _angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"].forChild(linuxRoutes)
            ],
            declarations: [],
            exports: [_angular_router__WEBPACK_IMPORTED_MODULE_4__["RouterModule"]],
            providers: [_auth_guard__WEBPACK_IMPORTED_MODULE_5__["AuthGuard"]]
        })
    ], LinuxRoutingModule);
    return LinuxRoutingModule;
}());



/***/ }),

/***/ "./src/app/linux/linux.component.css":
/*!*******************************************!*\
  !*** ./src/app/linux/linux.component.css ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\r\n\r\nnav {\r\n  background-color: #6c63ff;\r\n}\r\n\r\nnav ul a:hover {\r\n\r\nborder-bottom: 4px solid #6c63ff;\r\n}\r\n\r\n.logo {\r\n  height: 15%;\r\n  width: 15%;\r\n  margin-top: 17px\r\n  }\r\n\r\n.logo-text {\r\nposition: absolute;\r\npadding-left: 3px;\r\nfont-weight: 700;\r\nfont-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\r\nfont-size: 1.4rem;\r\n}\r\n\r\n.dropdown {\r\nposition: absolute;\r\n}\r\n\r\n.dropdown:hover {\r\nbackground-color: #6c63ff;\r\nborder-bottom: 4px solid #6c63ff;\r\n}\r\n\r\n.dropdown-content{\r\n  width: -webkit-max-content !important;\r\n  width: -moz-max-content !important;\r\n  width: max-content !important;\r\n  height:auto !important;\r\n}\r\n\r\n#video {\r\nmargin-right: 4px;\r\nmargin-left: 4px;\r\n}\r\n\r\n#lab {\r\nmargin-right: 4px;\r\nmargin-left: 4px;\r\n}\r\n\r\n#chat {\r\n  margin-right: 4px;\r\n  margin-left: 4px;\r\n}\r\n\r\n.lab_area {\r\n  border-radius: 20px;\r\n  border: 2px solid #cdd1d4de;\r\n  height: 400px;\r\n  width: 600px;\r\n  margin-left: 10px;\r\n}\r\n\r\n.course_topic {\r\n  background-color: black;\r\n  height: 35px;\r\n  text-align: center;\r\n  color: aliceblue;\r\n  font-weight: 400;\r\n  margin-top: 0px;\r\n  border-top-right-radius: 20px;\r\n  border-top-left-radius: 20px;\r\n}\r\n\r\n#message_box {\r\n  display: block!important;\r\n  height:1.7rem!important;\r\n  padding: .5rem!important;\r\n  border: 2px solid #636566de;\r\n  transition: all 1s;\r\n  border-radius: .5rem!important;\r\n  box-shadow: none;\r\n  width: 98%!important;\r\n}\r\n\r\n#submit {\r\n  height: 2.9rem!important;\r\n  border-top-right-radius: .5rem;\r\n  border-bottom-right-radius: .5rem;\r\n  -webkit-appearance: none;\r\n     -moz-appearance: none;\r\n          appearance: none;\r\n  margin-left: -50px;\r\n  padding-right: 10px;\r\n  border-right: 2px solid #636566de;\r\n  border-top: 2px solid #636566de;\r\n  border-bottom: 2px solid #636566de;\r\n  box-shadow: none;\r\n  padding-right: 10px;\r\n  padding-left: auto;\r\n  margin-bottom: 0px;\r\n}\r\n\r\n#send_icon {\r\n  margin-left: -10px;\r\n}\r\n"

/***/ }),

/***/ "./src/app/linux/linux.component.html":
/*!********************************************!*\
  !*** ./src/app/linux/linux.component.html ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n\n<div class=\"navbar \">\n  <nav>\n    <div class=\"nav-wrapper\">\n      <div class=\"container-fluid\">\n        <div class=\"row\">\n\n          <div class=\"col l3 m3 s3\">\n            <a class=\"brand-logo\"><img src=\"/src/assets/image/Final-Logo.png\" alt=\"nav-logo\" class=\"logo\"><span class=\"logo-text\">ClassRoom</span></a>\n          </div>\n\n          <div class=\"col l3 m3 s3\">\n            <a materialize=\"dropdown\" class=\"dropdown-button dropdown\" data-activates=\"dropdown1\" style=\"cursor: pointer;\">Linux Fundamentals<i class=\"material-icons right\">arrow_drop_down</i></a>\n            <!-- Dropdown Structure -->\n            <ul id=\"dropdown1\" class=\"dropdown-content\">\n                <li><a routerLink=\"/classroom\" routerLinkActive>Django</a></li>\n                <li class=\"divider\"></li>\n                <li><a >Linux Fundamentals</a></li>\n            </ul>\n\n          </div>\n\n            <div class=\"col l6 m6 s6\">\n              <ul class=\"right\">\n                <li><a>{{dataservice.username}}</a></li>\n                <li><a (click)=\"logout()\" id=\"logout\">LOGOUT</a></li>\n              </ul>\n            </div>\n        </div>\n      </div>\n    </div>\n  </nav>\n</div>\n\n<div class=\"container-fluid\">\n  <div class=\"row\">\n    <div class=\"col l3 m3 s3\" style=\"background-color:#4d394b; height: 100%;\">\n      <h6 style=\"text-align: center; font-weight: bold;\">Registered Students | {{users.length}}</h6>\n      <div style=\"height:450px; overflow: auto;\">\n        <ul>\n          <li id=\"students\" style=\"color:darkgrey; font-weight: bolder; font-size: 15px;\"\n              *ngFor=\"let user of users\"><a> {{ user.username }} </a>\n          </li><br>\n        </ul>\n      </div>\n    </div>\n    <div class=\"col l6 m6 s9\">\n      <ul style=\"display:flex;\">\n        <li><a routerLink= \"./videos\" routerLinkActive=\"active\" id=\"video\">Video</a></li> |\n        <li><a href= \"\" target=\"_blank\" id=\"lab\">Labs</a></li> |\n        <li><a [routerLink]=\"['./linux-chat']\" routerLinkActive=\"router-link-active\" id=\"chat\" > Chat</a></li>\n      </ul>\n      <hr>\n      <div style=\"max-height:600px; overflow: auto;\">\n        <router-outlet></router-outlet>\n      </div>\n    </div>\n    <div class=\"col l3 m3 s12\">\n      <div class=\"\">\n\n          <h5 style=\"text-align:center; font-weight: bolder;\">Topics</h5>\n          <div class=\"course_topic_area\" style=\"height: 450px; overflow: auto;\">\n          <ul class=\"collection\">\n\n              <li class=\"collection-item avatar\">\n                <i class=\"material-icons circle red\">play_arrow</i>\n\n                <a routerLink='./linux-chat'>Demo Topic Here</a>\n\n              </li>\n\n            </ul>\n          </div>\n        </div>\n    </div>\n  </div>\n</div>\n\n"

/***/ }),

/***/ "./src/app/linux/linux.component.ts":
/*!******************************************!*\
  !*** ./src/app/linux/linux.component.ts ***!
  \******************************************/
/*! exports provided: LinuxComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LinuxComponent", function() { return LinuxComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../data.service */ "./src/app/data.service.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm5/http.js");
/* harmony import */ var angular2_materialize__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! angular2-materialize */ "./node_modules/angular2-materialize/dist/index.js");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




var LinuxComponent = /** @class */ (function () {
    function LinuxComponent(dataservice, http, materializedirective) {
        this.dataservice = dataservice;
        this.http = http;
        this.materializedirective = materializedirective;
        this.users = [];
        this.options = {};
        this.dataservice.username = sessionStorage.getItem('username');
        this.dataservice.authOptions = {
            headers: new _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpHeaders"]({ 'Content-Type': 'application/json', 'Authorization': 'JWT ' + sessionStorage.getItem('token') })
        };
    }
    LinuxComponent.prototype.ngOnInit = function () {
        var _this = this;
        // this.dataservice.groupclassusers().subscribe((data: Array<object>) => {
        //   this.users = data;
        //   console.log(data);
        // });
        this.dataservice.djangostudents().subscribe(function (data) {
            _this.users = data;
        });
    };
    LinuxComponent.prototype.logout = function () {
        this.dataservice.logout();
    };
    LinuxComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-linux',
            template: __webpack_require__(/*! ./linux.component.html */ "./src/app/linux/linux.component.html"),
            styles: [__webpack_require__(/*! ./linux.component.css */ "./src/app/linux/linux.component.css")]
        }),
        __metadata("design:paramtypes", [_data_service__WEBPACK_IMPORTED_MODULE_1__["DataService"], _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"], angular2_materialize__WEBPACK_IMPORTED_MODULE_3__["MaterializeModule"]])
    ], LinuxComponent);
    return LinuxComponent;
}());



/***/ }),

/***/ "./src/app/login/login.component.css":
/*!*******************************************!*\
  !*** ./src/app/login/login.component.css ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "nav {\r\n    background-color:#6c63ff ;\r\n    box-shadow: none;\r\n    border-bottom: 1px;\r\n    \r\n}\r\n\r\n.nav-wrapper {\r\n  padding-left: 35px;\r\n  padding-right: 30px;\r\n}\r\n\r\n.logo {\r\n  height: 15%;\r\n  width: 15%;\r\n  margin-top: 17px\r\n  }\r\n\r\n.logo-text {\r\n  position: absolute;\r\n  padding-left: 3px;\r\n  font-weight: 700;\r\n  \r\n  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\r\n  font-size: 1.7rem;\r\n  \r\n  }\r\n\r\nnav ul a:hover {\r\n  \r\n  border-bottom: 4px solid #6c63ff;\r\n}\r\n\r\n#login_username {\r\n    display: block!important;\r\n    height:1.82rem!important;\r\n    padding: .5rem!important;\r\n    border: 1px solid #cdd1d4de;\r\n    transition: all 1s;\r\n    border-radius: .25rem!important;\r\n    box-shadow: none;\r\n    width: 96%!important;\r\n  }\r\n\r\n#login_password {\r\n    display: block!important;\r\n    height:1.82rem!important;\r\n    padding: .5rem!important;\r\n    border: 1px solid #cdd1d4de;\r\n    transition: all 1s;\r\n    border-radius: .25rem!important;\r\n    box-shadow: none;\r\n    width: 96%!important;\r\n  }\r\n\r\n#login_project {\r\n    display: block!important;\r\n    height:1.82rem!important;\r\n    padding: .5rem!important;\r\n    border: 1px solid #cdd1d4de;\r\n    transition: all 1s;\r\n    border-radius: .25rem!important;\r\n    box-shadow: none;\r\n    width: 96%!important;\r\n  }\r\n\r\n.submit {\r\n    width:100%!important;\r\n    background-color:#6c63ff\r\n  }\r\n\r\n#home_login {\r\n      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\r\n      font-size: 1.2rem;\r\n      font-weight: bolder;\r\n      color: rgba(90, 84, 84, 0.61);\r\n  }\r\n\r\na {\r\n      text-decoration: none;\r\n  }\r\n\r\n.click {\r\n      font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;\r\n      text-align: center;\r\n      \r\n      margin-right: auto;\r\n      margin-left: auto;\r\n  }"

/***/ }),

/***/ "./src/app/login/login.component.html":
/*!********************************************!*\
  !*** ./src/app/login/login.component.html ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"navbar \">\n    <nav>\n      <div class=\"nav-wrapper\">\n        <div class=\"container-fluid\">\n            <a routerLink=\"\" routerLinkActive class=\"brand-logo\"><img src=\"/src/assets/image/Final-Logo.png\" alt=\"nav-logo\" class=\"logo\"><span class=\"logo-text\">ClassRoom</span></a>\n          <ul class=\"right hide-on-med-and-down\">\n            <li><a routerLink=\"/signup\" routerLinkActive>REGISTER</a></li>\n            <li><a routerLink=\"/login\"routerLinkActive id=\"logout\">LOGIN</a></li>\n          </ul>\n        </div>\n      </div>\n    </nav>\n  </div>\n\n\n<div class=\"\">\n  <div class=\"container-fluid\">\n      <div class=\"row\">\n      <div class=\"col m4\"></div>\n      <div class=\"col m4\">\n          <p><strong> {{dataservice.message}}</strong></p>\n          <h4 class=\"bold center\" id=\"login_header\">LOGIN</h4>\n\n          <form (ngSubmit)=\"login()\">\n              <div class=\"form-group\">\n                  <input required=\"required\" class=\"form-control\" type=\"text\" id=\"login_username\" [(ngModel)]=\"dataservice.login_username\" name=\"login_username\" placeholder=\"Username\">\n              </div>\n              <br>\n              <div class=\"form-group\">\n                  <input required=\"required\" class=\"form-control\" type=\"password\" id=\"login_password\" [(ngModel)]=\"dataservice.login_password\" name=\"login_password\" placeholder=\"Password\">\n              </div>\n              <br>\n              <div class=\"form-group\">\n                  <input class=\"form-control btn btn-default submit\" type=\"submit\" value=\"Login\">\n              </div>\n          </form>\n          <br>\n\n      </div>\n      <div class=\"col m4\"></div>\n      </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/login/login.component.ts":
/*!******************************************!*\
  !*** ./src/app/login/login.component.ts ***!
  \******************************************/
/*! exports provided: LoginComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LoginComponent", function() { return LoginComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../data.service */ "./src/app/data.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var LoginComponent = /** @class */ (function () {
    function LoginComponent(router, dataservice) {
        this.router = router;
        this.dataservice = dataservice;
    }
    LoginComponent.prototype.ngOnInit = function () {
    };
    LoginComponent.prototype.toUser = function () {
        this.router.navigate(['signup']);
        this.dataservice.message = '';
    };
    LoginComponent.prototype.login = function () {
        this.dataservice.login();
    };
    LoginComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-login',
            template: __webpack_require__(/*! ./login.component.html */ "./src/app/login/login.component.html"),
            styles: [__webpack_require__(/*! ./login.component.css */ "./src/app/login/login.component.css")]
        }),
        __metadata("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_1__["Router"], _data_service__WEBPACK_IMPORTED_MODULE_2__["DataService"]])
    ], LoginComponent);
    return LoginComponent;
}());



/***/ }),

/***/ "./src/app/signup/signup.component.css":
/*!*********************************************!*\
  !*** ./src/app/signup/signup.component.css ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "nav {\r\n    background-color:#6c63ff ;\r\n    box-shadow: none;\r\n    border-bottom: 1px;\r\n    \r\n}\r\n\r\n.nav-wrapper {\r\n  padding-left: 35px;\r\n  padding-right: 30px;\r\n}\r\n\r\n.logo {\r\n  height: 15%;\r\n  width: 15%;\r\n  margin-top: 17px\r\n  }\r\n\r\n.logo-text {\r\n  position: absolute;\r\n  padding-left: 3px;\r\n  font-weight: 700;\r\n  \r\n  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\r\n  font-size: 1.7rem;\r\n  \r\n  }\r\n\r\nnav ul a:hover {\r\n  \r\n  border-bottom: 4px solid #6c63ff;\r\n}\r\n\r\n#username {\r\n    display: block!important;\r\n    height:1.82rem!important;\r\n    padding: .5rem!important;\r\n    border: 1px solid #cdd1d4de;\r\n    transition: all 1s;\r\n    border-radius: .25rem!important;\r\n    box-shadow: none;\r\n    width: 96%!important;\r\n  }\r\n\r\n#password {\r\n    display: block!important;\r\n    height:1.82rem!important;\r\n    padding: .5rem!important;\r\n    border: 1px solid #cdd1d4de;\r\n    transition: all 1s;\r\n    border-radius: .25rem!important;\r\n    box-shadow: none;\r\n    width: 96%!important;\r\n  }\r\n\r\n#email {\r\n    display: block!important;\r\n    height:1.82rem!important;\r\n    padding: .5rem!important;\r\n    border: 1px solid #cdd1d4de;\r\n    transition: all 1s;\r\n    border-radius: .25rem!important;\r\n    box-shadow: none;\r\n    width: 96%!important;\r\n  }\r\n\r\n.submit {\r\n    width:100%!important;\r\n    background-color:#6c63ff\r\n  }\r\n\r\n#home_login {\r\n      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;\r\n      font-size: 1.2rem;\r\n      font-weight: bolder;\r\n      color: rgba(90, 84, 84, 0.61);\r\n  }\r\n\r\na {\r\n      text-decoration: none;\r\n  }\r\n\r\n.click {\r\n      font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;\r\n      text-align: center;\r\n      \r\n      margin-right: auto;\r\n      margin-left: auto;\r\n  }"

/***/ }),

/***/ "./src/app/signup/signup.component.html":
/*!**********************************************!*\
  !*** ./src/app/signup/signup.component.html ***!
  \**********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div class=\"navbar \">\n    <nav>\n      <div class=\"nav-wrapper\">\n        <div class=\"container-fluid\">\n            <a routerLink=\"\" routerLinkActive class=\"brand-logo\"><img src=\"/src/assets/image/Final-Logo.png\" alt=\"nav-logo\" class=\"logo\"><span class=\"logo-text\">ClassRoom</span></a>\n          <ul class=\"right hide-on-med-and-down\">\n            <li><a routerLink=\"/signup\" routerLinkActive>REGISTER</a></li>\n            <li><a routerLink=\"/login\" routerLinkActive>LOGIN</a></li>\n          </ul>\n        </div>\n      </div>\n    </nav>\n  </div>\n\n\n<div class=\"\">\n  <div class=\"container-fluid\">\n      <div class=\"row\">\n      <div class=\"col m4\"></div>\n      <div class=\"col m4\">\n          <p>{{dataservice.message}}</p>\n          <h4 class=\"bold center\" id=\"signUpheader\">SIGN-UP</h4>\n\n          <form (ngSubmit)=\"createUser()\" id=\"signUp\">\n              <div class=\"form-group\">\n                  <input required=\"required\" class=\"form-control\" type=\"text\" id=\"email\" [(ngModel)]=\"dataservice.createuser_email\" name=\"email\" placeholder=\"Email\" required>\n              </div>\n              <br>\n              <div class=\"form-group\">\n                  <input required=\"required\" class=\"form-control\" type=\"password\" id=\"password\" [(ngModel)]=\"dataservice.createuser_password\" name=\"password\" placeholder=\"Password\" required>\n              </div>\n              <br>\n              <div class=\"form-group\">\n                  <input required=\"required\" class=\"form-control\" type=\"text\" id=\"username\" [(ngModel)]=\"dataservice.createuser_username\" name=\"username\" placeholder=\"Username\" required>\n              </div>\n\n              <input class=\"btn btn-default submit\" type=\"submit\" value=\"Sign Up\" id=\"create_user\">\n          </form>\n      </div>\n      <div class=\"col m4\"></div>\n      </div>\n  </div>\n</div>\n"

/***/ }),

/***/ "./src/app/signup/signup.component.ts":
/*!********************************************!*\
  !*** ./src/app/signup/signup.component.ts ***!
  \********************************************/
/*! exports provided: SignupComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SignupComponent", function() { return SignupComponent; });
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm5/router.js");
/* harmony import */ var _data_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../data.service */ "./src/app/data.service.ts");
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (undefined && undefined.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



var SignupComponent = /** @class */ (function () {
    function SignupComponent(router, dataservice) {
        this.router = router;
        this.dataservice = dataservice;
    }
    SignupComponent.prototype.ngOnInit = function () {
    };
    SignupComponent.prototype.toLogin = function () {
        this.router.navigate(['login']);
    };
    SignupComponent.prototype.createUser = function () {
        this.dataservice.createUser();
        this.dataservice.message = '';
    };
    SignupComponent = __decorate([
        Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["Component"])({
            selector: 'app-signup',
            template: __webpack_require__(/*! ./signup.component.html */ "./src/app/signup/signup.component.html"),
            styles: [__webpack_require__(/*! ./signup.component.css */ "./src/app/signup/signup.component.css")]
        }),
        __metadata("design:paramtypes", [_angular_router__WEBPACK_IMPORTED_MODULE_1__["Router"], _data_service__WEBPACK_IMPORTED_MODULE_2__["DataService"]])
    ], SignupComponent);
    return SignupComponent;
}());



/***/ }),

/***/ "./src/environments/environment.ts":
/*!*****************************************!*\
  !*** ./src/environments/environment.ts ***!
  \*****************************************/
/*! exports provided: environment */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "environment", function() { return environment; });
// This file can be replaced during build by using the `fileReplacements` array.
// `ng build ---prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.
var environment = {
    production: false
};
/*
 * In development mode, for easier debugging, you can ignore zone related error
 * stack frames such as `zone.run`/`zoneDelegate.invokeTask` by importing the
 * below file. Don't forget to comment it out in production mode
 * because it will have a performance impact when errors are thrown
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.


/***/ }),

/***/ "./src/main.ts":
/*!*********************!*\
  !*** ./src/main.ts ***!
  \*********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm5/core.js");
/* harmony import */ var _angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser-dynamic */ "./node_modules/@angular/platform-browser-dynamic/fesm5/platform-browser-dynamic.js");
/* harmony import */ var _app_app_module__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./app/app.module */ "./src/app/app.module.ts");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./environments/environment */ "./src/environments/environment.ts");




if (_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].production) {
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_0__["enableProdMode"])();
}
Object(_angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_1__["platformBrowserDynamic"])().bootstrapModule(_app_app_module__WEBPACK_IMPORTED_MODULE_2__["AppModule"])
    .catch(function (err) { return console.log(err); });


/***/ }),

/***/ 0:
/*!***************************!*\
  !*** multi ./src/main.ts ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! C:\Users\Jide\Desktop\Training\Projects\AngularProject\groupclass2\src\main.ts */"./src/main.ts");


/***/ })

},[[0,"runtime","vendor"]]]);
//# sourceMappingURL=main.js.map