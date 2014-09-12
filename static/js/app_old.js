/*  FB.init({
    appId      : '490262681101649',
    status     : true,
    xfbml      : true,
    version    : 'v2.0',
  });
*/

    if(document.location.hostname!="127.0.0.1"){
        var DOMAIN = "http://rentlisting-snowleo.rhcloud.com";
    }
    else{
        var DOMAIN = "http://127.0.0.1:8000";
    }

var ajaxCall = angular.module('ajaxCall', ['ngResource']);

ajaxCall.factory('Phone', ['$resource',
  function($resource){
    return $resource('phones/:phoneId.json', {}, {
      query: {method:'GET', params:{phoneId:'phones'}, isArray:true}
    });
  }]);



var app = angular.module("app", [
    'ngRoute',
    'ajaxCall'
    
]);

app.controller('ctrl_main', ['$scope', '$http',
  function ($scope, $http) {
    $http.get('phones/phones.json').success(function(data) {
      $scope.phones = data;
    });

    $scope.orderProp = 'age';
  }]);

$(function () {
    // SETUP
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    var csrftoken = $.cookie('csrftoken');
    $.ajaxSetup({
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
        xhrFields: {
            withCredentials: true
        },
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });

    // CONSTANT
    if(document.location.hostname!="127.0.0.1"){
        var DOMAIN = "http://rentlisting-snowleo.rhcloud.com";
    }
    else{
        var DOMAIN = "http://127.0.0.1:8000";
    }
    // AJAX
    var ajaxCall = {
        login: function (username, password) {
            var postdata = {};

            postdata.username = username;
            postdata.password = password;
            return $resource(DOMAIN + /login/, postdata);
        },
        create_account: function (username, password,password2) {
            var postdata = {};

            postdata.username = username;
            postdata.pw = password;
            postdata.pw_2 = password2;
            return $.post(DOMAIN + '/login/create/', postdata);
        },
        confirm_email: function (postdata) {
            console.log("confirm email call");
            return $.post(DOMAIN + '/login/confirm_email/', postdata);
        },        
        logout: function (user_id) {
            var postdata = {};
            postdata.user_id = user_id;
            return $.post(DOMAIN + '/login/logout/', postdata);
        },
        check_login: function () {
            var postdata = {};
            return $.post(DOMAIN + '/login/check_login/', postdata);
        },
        get_feature_post: function () {
            var postdata = {};
            return $.post(DOMAIN + '/polls/get_feature_post/', postdata);
        },        
        search: function (postdata) {
            return $.post(DOMAIN + '/polls/search/', postdata);
        },
        event: function (event_id) {
            var postdata = {};
            postdata.event_id = event_id;
            return $.post(DOMAIN + '/polls/event_query/', postdata);
        },
        resorts: function () {
            var postdata = {};
            return $.post(DOMAIN + '/polls/ski_resort_list/', postdata);
        },
        meetup_places: function () {
            var postdata = {};
            return $.post(DOMAIN + '/polls/meetup_place_list/', postdata);
        },
        join_event: function (event_id, guest_num, ski_num, sb_num) {
            var postdata = {};
            postdata.event_id = event_id;
            postdata.guest_num = parseInt(guest_num || 1, 10);
            postdata.ski_num = parseInt(ski_num || 0, 10);
            postdata.sb_num = parseInt(sb_num || 0, 10);
            console.log(postdata);
            return $.post(DOMAIN + '/polls/join_event/', postdata);
        },
        post_event: function (postdata) {
            return $.post(DOMAIN + '/polls/post_event/', postdata);
        },
        delete_event: function (event_id) {
            var postdata = {};
            postdata.event_id = event_id;
            console.log(postdata);
            return $.post(DOMAIN + '/polls/delete_event/', postdata);
        },
        comment_event: function (event_id, comment) {
            var postdata = {};
            postdata.event_id = event_id;
            postdata.comment = comment;
            console.log(postdata);
            return $.post(DOMAIN + '/polls/comment_event/', postdata);
        },
        ask_poster_question: function (event_id, question, giver_pk, receiver_pk) {
            var postdata = {};
            postdata.event_id = event_id;
            postdata.question=question;
            postdata.giver_pk=giver_pk;
            postdata.receiver_pk=receiver_pk;
            console.log(postdata);
            return $.post(DOMAIN + '/polls/ask_poster_question/', postdata);
        },
        get_conversation: function (event_id, questioner_id) {
            var postdata = {};
            postdata.event_id = event_id;
            postdata.questioner_id=questioner_id;
            console.log(postdata);
            return $.post(DOMAIN + '/polls/get_question_conversation/', postdata);
        },
        set_read_notice: function (notice_id) {
            var postdata = {};
            postdata.notice_id = notice_id;
            console.log(postdata);
            return $.post(DOMAIN + '/login/set_read_notice/', postdata);
        }
    };

    // UTILITY
    function Void() {}; // void function

    // OBJECT
    function Option(text, value) {
        this.text = text;
        this.value = value || text;
    }

    function OptionText(item) {
        return item.text;
    }

    function poll(p, app) {
        if ( !! p.fields) {
            p.fields.pk = p.pk;
            p = p.fields;
        }
        p.pub_date = new Date(p.pub_date);
        p.start_date = new Date(p.start_date);
        p.end_date = new Date(p.end_date);
        p.zip = parseInt(p.zip, 10);
        p.user_pk = parseInt(p.user_pk, 10);
        return p;
    }

    function detail(d, app) {
        d.poll = poll(d.poll, app);
       // $.map(d.passanger, function (p) {
    //        p.guest_num = parseInt(p.guest_num, 10);
      //  });
        return d;
    }

    function User(app) {
        var self = this;
        self.last_name = ko.observable();
        self.username = ko.observable();
        self.password = ko.observable();
        self.password2 = ko.observable();
        self.user_id = ko.observable();
        self.profile_pic = ko.observable();
        self.error_msg=ko.observable();
        self.user_unread_notice_number=ko.observable();
        self.notices = ko.observableArray();
        self.conversations = ko.observableArray();
        self.go2login = function () {
            app.viewChange('login');
        };
        self.go2Create = function () {
            app.viewChange('create_account');
        };
        self.doLogin = function () {
            if ( !! self.username() && !! self.password()) {
                ajaxCall.login(self.username(), self.password()).done(function (id) {
                    self.user_id(id);
                    parent.$.fancybox.close();
                    window.history.go(-1)
                });
            }
        };
        self.doCreate = function () {
            if(self.password()!=self.password2()){
                self.error_msg='please check password';}
            else if ( !! self.username() && !! self.password()) {
                ajaxCall.create_account(self.username(), self.password(), self.password2).done(function (id) {
                    self.user_id(id);
//                    app.viewChange('search');
                    window.history.go(-2)
                });
            }
        };        
        self.checkLogin = function () {
            ajaxCall.check_login().done(function (user) {
                self.username(user.username);
                self.user_id(user.id);
                self.profile_pic(user.profile_pic)
                self.notices(user.notice);
                console.log(user.profile_pic);
                self.user_unread_notice_number(user.un_read_notice_num);
            });
        }
        self.confirm_email = function () {
            ajaxCall.confirm_email().done(function (log) {
                console.log(log);
            });
        }
        self.click_event= function(notice){
            app.viewChange('event', {
                id: notice.post_id
            });
        }
        self.click_conversation= function(notice){
            ajaxCall.set_read_notice(notice.notice_pk).done(function (log) {
                console.log(log);
            });                  
            /*ajaxCall.get_conversation(notice.post_id,notice.notice_giver_id).done(function (data) {
                self.conversations(data);
            });                  */
            app.viewChange('conversation_page',{
                post_id: notice.post_id,
                asker_id: notice.notice_giver_id
            });
        }        
        self.doLogout = function () {
            ajaxCall.logout(self.user_id()).done(function (log) {
                console.log('logout');
                //window.location.reload();
                self.user_id('');
            });
        };
        self.back = function () {
            //app.viewChange('search');
            window.history.go(-1)
        };
    }

    function Resorts() {
        var self = this;
        self.list = ko.observableArray();
        self.options = ko.computed(function () {
            return $.map(self.list(), function (r) {
                return new Option(r.name, r.id)
            });
        });
        self.get = function () {
            return ajaxCall.resorts().done(function (raw) {
                self.list($.map(raw, function (r) {
                    r.fields.id = r.pk;
                    return r.fields;
                }));
            });
        };
    }

    function Meetups() {
        var self = this;
        self.list = ko.observableArray();
        self.options = ko.computed(function () {
            return $.map(self.list(), function (r) {
                return new Option(r.name, r.id)
            });
        });
        self.get = function () {
            return ajaxCall.meetup_places().done(function (raw) {
                self.list($.map(raw, function (r) {
                    r.fields.id = r.pk;
                    return r.fields;
                }));
            });
        };
    }

    // VIEW
    function View(app, name) {
        var self = this;
        self.app = app;
        self.name = ko.observable(name);
        self.body = ko.observable('view_' + name);
        self.intent = ko.observable();
        // method
        self.init = Void;
        return self;
    }

    function View_login(app) {
        var self = new View(app, 'login');
        self.user = app.user;
        return self;
    }
    function View_create_account(app) {
        var self = new View(app, 'create_account');
        self.user = app.user;
        return self;
    }    
    function View_notice_page(app) {
        var self = new View(app, 'notice_page');
        self.user = app.user;
        self.user.checkLogin();
        

        return self;
    }        
app.controller('ctrl_notice_page', ['$scope', '$routeParams',
  function($scope, $routeParams) {
    $scope.phoneId = $routeParams.phoneId;
  }]);    
    function View_conversation_page(app) {
        var self = new View(app, 'conversation_page');
        self.user = app.user;
        self.conversations=ko.observableArray();
        self.post_id= ko.observable();
        self.asker_id= ko.observable();
        
        self.reply_conversation=ko.observable();
        //self.asker_id('Leo');

        self.send_reply_conversation = function () {
            ajaxCall.ask_poster_question(self.post_id(),self.reply_conversation(),self.user.user_id(),self.asker_id())
                    .done(function (result) {
                        console.log(result);
                        self.getDetail();
                    });
        }
        self.getDetail = function () {
            var post_id=self.post_id();
            var asker_id=self.asker_id();
            if ( !! post_id && !!asker_id) {
                ajaxCall.get_conversation(post_id,asker_id).done(function (data) {
                    self.conversations(data);
                    console.log(self.conversations());
                    console.log(self.asker_id());
                    console.log(self.post_id());
                })
            }
        };
        
        self.asker_id.subscribe(self.getDetail);
        //self.click_conversation(self.post_id(),self.asker_id());
          self.intent.subscribe(function (intent) {
            if ( !! intent.post_id) {
                self.post_id(intent.post_id);
                console.log("post_id "+self.post_id());                
            }
            if ( !! intent.asker_id) {
                self.asker_id(intent.asker_id);
                console.log("asker_id "+self.asker_id());                
            }
  
        });        

        return self;
    }        
    function View_main(app) {
        var self = new View(app, 'main');
        self.user = app.user;
//        self.search_zip=ko.observable(95050); 
//        self.intent=ko.observable(); 
        self.search_result = function () {
//            console.log('main:'+self.search_zip());
            app.viewChange('search');
        }         
        return self;
    }    
    function View_search(app) {
        var self = new View(app, 'search');
    self.rent_max = ko.observable(10);
    self.rent_min = ko.observable(5);
    self.range_max = ko.observable(0);       
    self.range_min = ko.observable(0);    
    self.sel_bed_num = ko.observable(0);    
    self.bed_range_max = ko.observable(0);       
    self.bed_range_min = ko.observable(0);         
    self.sel_bath_num = ko.observable(0);     
    self.bath_range_max = ko.observable(0);       
    self.bath_range_min = ko.observable(0);         
    self.polls_filter_len= ko.observable(0);  
    self.search_zip=ko.observable();  


        self.polls = ko.observableArray([]);
    self.polls_filter = ko.computed(function() {
        return ko.utils.arrayFilter(self.polls(), function(item) {
//            console.debug('polls_filter');
//            console.debug(item);
            return item.rent >= self.rent_min() && item.rent <= self.rent_max() &&
                (item.num_bed== self.sel_bed_num() || self.sel_bed_num()==0) &&
                (item.num_bath== self.sel_bath_num() || self.sel_bath_num()==0);
//             return item.rent >=0;
        });
    });  
    
        self.loading = ko.observable(false);
        self.resort = ko.observable();
        self.start_date = ko.observable();
        // methods
        self.update = ko.computed(function () {
            var postdata = {};
            var search_zip=app.search_zip;
//            console.log(search_zip);
            if ( !! search_zip) {
                postdata.search_zip = search_zip;
            }
            if ( !! self.start_date()) {
                postdata.start_date = self.start_date();
            }
            //send request
//            if(search_zip!=null){
                self.loading(true);
                ajaxCall.search(postdata).done(function (raw) {
                    self.polls($.map(raw, function (p) {
                        return poll(p, app);
                    }));
                    console.log(self.polls());
                    var max=0;
                    var min=0;
                    var bed_max=0;
                    var bed_min=0;
                    var bath_max=0;
                    var bath_min=0;
                    for (var i = 0; i < raw.length; i++) { 
                        if(max< raw[i].rent){max= raw[i].rent;}
                        if(min==0){min= raw[i].rent;}
                        else if(min> raw[i].rent){min= raw[i].rent;}
    
                        if(bed_max< raw[i].num_bed){bed_max= raw[i].num_bed;}
                        if(bed_min==0){bed_min= raw[i].num_bed;}
                        else if(bed_min> raw[i].num_bed){bed_min= raw[i].num_bed;}
                        
                        if(bath_max< raw[i].num_bath){bath_max= raw[i].num_bath;}
                        if(bath_min==0){bath_min= raw[i].num_bath;}
                        else if(bath_min> raw[i].num_bath){bath_min= raw[i].num_bath;}                    
                    }
                    self.range_max(max);self.rent_max(max);
                    self.range_min(min);self.rent_min(min);   
                    self.bed_range_max(bed_max);self.bed_range_min(bed_min);
                    self.bath_range_max(bath_max);self.bath_range_min(bath_min);
                    self.loading(false);
                 });
//                }
        }).extend({
            throttle: 500
        });
        self.click = function (poll) {
            app.viewChange('event', {
                id: poll.pk
            });
        };
        self.back = function () {
            app.viewChange('main');
        };
        self.reset_filter = function () {
            self.rent_max(self.range_max());
            self.rent_min(self.range_min()); 
            self.sel_bed_num(0);
            self.sel_bath_num(0);
        };      
//        self.search_zip.subscribe(self.update);
        // intent
        self.intent.subscribe(function (intent) {
            if ( !! intent.search_zip) {
                self.search_zip(intent.search_zip);
                console.log(self.search_zip());                
            }

        });        
//       self.range_max= ko.computed(function() {
//           var max=0;
//           for (var i = 0; i < self.polls.length; i++) { 
//               if(max< self.polls[i].rent){
//                   max= self.polls[i].rent;
//               }
//           }
//           return max;
//       });   
        return self;
    }

    function View_event(app) {
        var self = new View(app, 'event');
        self.loading = ko.observable(false);
        self.event_id = ko.observable();
        self.poll = ko.observable();
        self.passengers = ko.observableArray();
        self.comments = ko.observableArray();
        self.user_id = app.user.user_id;
        self.textarea_comment = ko.observable();
        self.image1 = ko.observable();	
        self.up_load_domain= ko.observable(DOMAIN+'/polls/add_pic/');
        self.room_pic=ko.observable();
        self.ask_q_context=ko.observable();

        self.imgs = ko.observableArray();

        self.showComment = ko.computed(function () {
            //return !!self.user_id();
            return true;
        });
        self.showJoin = ko.computed(function () {
            var show = false;
            if ( !! self.user_id() && !! self.poll()) {
                show = self.user_id() !== self.poll().user_pk;
            }
            return show;
        });
        self.showEdit = ko.computed(function () {
            var show = false;
            if ( !! self.user_id() && !! self.poll()) {
                show = self.user_id() == self.poll().user_pk;
            }
            return show;
        });

        //methods
        self.back = function () {
            window.history.go(-1)
        };
        self.getDetail = function () {
            self.loading(true);
            var event_id = self.event_id();
            if ( !! event_id) {
                ajaxCall.event(event_id).done(function (raw) {
                    console.log(raw);
                    var d = detail(raw, app);
                    self.poll(d.poll);
                    self.passengers(d.passanger);
                    self.comments(d.comment);
                    self.loading(false);
                });
            }
        };
        self.event_id.subscribe(self.getDetail);

        self.join = function () {
            ajaxCall.join_event(
                self.event_id(),
                self.guest_num(),
                self.ski_num(),
                self.sb_num()
            ).done(function (result) {
                self.getDetail();
            });
        }
        self.remove = function () {
            ajaxCall.delete_event(
                self.event_id()
            ).done(function (result) {
                self.back();
            });

        }
        self.edit = function () {
            console.log(self.event_id());
            app.viewChange('post', {
                id: self.event_id()
            });
        }        
        self.leaveComment = function () {
            if ( !! self.textarea_comment() && !! self.user_id()) {
            ajaxCall.comment_event(self.event_id(), self.textarea_comment())
                    .done(function (result) {
                        console.log(result);
                        self.textarea_comment('');
                        self.getDetail();
                    });
            }
        }
        
        self.ask_poster_question = function () {
            if ( !! self.user_id()) {
            ajaxCall.ask_poster_question(self.event_id(),self.ask_q_context(),self.user_id(),self.poll().user_pk)
                    .done(function (result) {
                        console.log(result);
                    });
                app.viewChange('conversation_page',{
                post_id: self.event_id(),
                asker_id: self.user_id()    
            });    
            }
        }
                        

        // intent
        self.intent.subscribe(function (intent) {
            if ( !! intent.id) {
                self.event_id(intent.id);
            }

        });
        return self;
    }

app_view_control.controller('ctrl_event', ['$scope', '$routeParams',
  function($scope, $routeParams) {
    $scope.event_id = $routeParams.id;
  }]);

    function View_post(app) {
        var self = new View(app, 'post');
        self.user_id = app.user.user_id;
        self.event_id = ko.observable();        
        self.departure_time = ko.observable(); 
        self.return_time = ko.observable();
        self.num_bed = ko.observable();
        self.num_bath = ko.observable();
        self.city = ko.observable();        
        self.address = ko.observable();
        self.state = ko.observable();
        self.zip = ko.observable();
        self.rent = ko.observable();
        self.content = ko.observable('');

        self.size                = ko.observable('');
        self.property_type       = ko.observableArray(['Single family house', 'Townhouse', 'Condo', 'Apartment']);
        self.floor_level         = ko.observable('');
        self.parking             = ko.observableArray(['No', 'Garage', 'Cover top']);
        self.pet                 = ko.observableArray(['No', 'Cat', 'Dog', 'both']);
        self.smoking               = ko.observable('');
        self.private_bath        = ko.observable('');
        self.washer_dryer        = ko.observableArray(['In unit', 'In community', 'No']);
        self.kitchen_access      = ko.observable('');
        self.internet            = ko.observable('');
        self.cable_tv            = ko.observable('');

        self.park                = ko.observable('');
        self.play_ground         = ko.observable('');
        self.tennis              = ko.observable('');
        self.basketball          = ko.observable('');
        self.swim_pool           = ko.observable('');
        self.jacuzzi             = ko.observable('');
        self.gym                 = ko.observable('');
        self.bbq_area            = ko.observable('');

        self.rent_internet       = ko.observable('');
        self.rent_cable_tv       = ko.observable('');
        self.rent_water          = ko.observable('');
        self.rent_gas            = ko.observable('');
        self.rent_electricity    = ko.observable('');
        self.rent_garbage        = ko.observable('');
        self.rent_parking        = ko.observable('');
        
        self.departure_time_check = ko.observable(); 
        self.return_time_check = ko.observable();
        self.num_bed_check = ko.observable();
        self.num_bath_check = ko.observable();
        self.city_check = ko.observable();        
        self.address_check = ko.observable();
        self.state_check = ko.observable();
        self.zip_check = ko.observable();
        self.rent_check = ko.observable();
        self.content_check = ko.observable('');
        
        
        self.getDetail = function () {
            self.loading(true);
            var event_id = self.event_id();
            if ( !! event_id) {
                ajaxCall.event(event_id).done(function (raw) {
                    console.log(raw);
                    var d = detail(raw, app);
                    self.poll(d.poll);
                    self.passengers(d.passanger);
                    self.comments(d.comment);
                    self.loading(false);
                });
            }
        };
        
        self.event_id.subscribe(View_event.getDetail);
        self.validate = ko.computed(function () {
            return !!self.departure_time() && !! self.return_time()

        });
        self.post_check_pass = function (){
            self.departure_time_check("");
            self.return_time_check("");
            self.num_bed_check("");
            self.num_bath_check("");
            self.city_check("");       
            self.address_check("");
            self.state_check("");
            self.zip_check("");
            self.rent_check("");
            self.content_check("");  
           if (!self.user_id())
           {
               self.content_check("please login before post")
               return 0;
           }                     
           else if (!self.departure_time())
           {
               self.departure_time_check("please enter start date")
               return 0;
           }
           else if (!self.return_time())
           {
               self.return_time_check("please enter end date")
               return 0;
           }       
           else if (!self.num_bed())
           {
               self.num_bed_check("please enter number of bed")
               return 0;
           }    
           else if (!self.num_bath())
           {
               self.num_bath_check("please enter number of bath")
               return 0;
           }  
           else if (!self.address())
           {
               self.address_check("please enter address")
               return 0;
           }                
           else if (!self.city())
           {
               self.city_check("please enter city")
               return 0;
           }    
           else if (!self.state())
           {
               self.state_check("please enter state")
               return 0;
           }    
           else if (!self.zip())
           {
               self.zip_check("please enter zip")
               return 0;
           }    
           else if (!self.rent())
           {
               self.rent_check("please enter rent")
               return 0;
           } 
           else if (!self.content())
           {
               self.content_check("please enter content")
               return 0;
           }     
            
            else
            {
                return 1;
            }
            
        }        

        self.post = function () {
            var postdata = {};
            postdata.departure_time = self.departure_time();
            postdata.return_time = self.return_time();
            postdata.num_bed = self.num_bed();
            postdata.num_bath = self.num_bath();
            postdata.city = self.city();            
            postdata.address = self.address();
            postdata.state = self.state();
            postdata.zip = self.zip();
            postdata.rent = self.rent();
            postdata.content = self.content();
            postdata.image = self.content();
            postdata.size=self.size();
            postdata.property_type=self.property_type();
            postdata.floor_level=self.floor_level();
            postdata.parking=self.parking();
            postdata.pet=self.pet();
            postdata.smoking=self.smoking();
            postdata.private_bath=self.private_bath();
            postdata.washer_dryer=self.washer_dryer();
            postdata.kitchen_access=self.kitchen_access();
            postdata.internet=self.internet();
            postdata.cable_tv=self.cable_tv();
            postdata.park=self.park();
            postdata.play_ground=self.play_ground();
            postdata.tennis=self.tennis();
            postdata.basketball=self.basketball();
            postdata.swim_pool=self.swim_pool();
            postdata.jacuzzi=self.jacuzzi();
            postdata.gym=self.gym();
            postdata.bbq_area=self.bbq_area();
            postdata.rent_internet=self.rent_internet();
            postdata.rent_cable_tv=self.rent_cable_tv();
            postdata.rent_water=self.rent_water();
            postdata.rent_gas=self.rent_gas();
            postdata.rent_electricity=self.rent_electricity();
            postdata.rent_garbage=self.rent_garbage();
            postdata.rent_parking=self.rent_parking();            
            console.log( postdata.departure_time)
            if(self.post_check_pass()){
            ajaxCall.post_event(postdata).done(function (id) {
                
                console.log(id);
                app.viewChange('event', {
                    id: id
                });
                

            });
            }
        };
        

        
        self.back = function () {
            window.history.go(-1)
        };
        self.init = function (el) {
            var $view = $(el).parents('.view'),
                $depart = $view.find('.date.departure'),
                $return = $view.find('.date.return');
            
            $return.datepicker({dateFormat: "yy-mm-dd"});
            $depart.datepicker({dateFormat: "yy-mm-dd"});
/*
            $return.datepicker({
                minDate: new Date(),
                dateFormat: "yy-mm-dd"
            }).datepicker('setDate', new Date()).change();

            $depart.datepicker({
                minDate: new Date(),
                dateFormat: "yy-mm-dd"
            }).datepicker('setDate', new Date()).change(function () {
                $return.datepicker("option", 'minDate', $(this).datepicker('getDate')).change();
            }).change();
*/
        }
        

        return self;
    }

    //APP
    function App() {
        var self = this,
            views = {
                login: View_login,
                search: View_search,
                event: View_event,
                post: View_post,
                create_account: View_create_account,
                notice_page: View_notice_page,
                conversation_page: View_conversation_page,
                main: View_main
            },
            vms = {};

        // observables
        self.view = ko.observable();
        self.VM = ko.observable();
        self.vms = {};
        self.user = new User(self);
        self.search_zip=ko.observable();
        self.feature_posts = ko.observableArray();
        self.feature_posts_0=ko.observable();
        self.feature_posts_1=ko.observable();
        self.feature_posts_2=ko.observable();
        self.feature_posts_3=ko.observable();
        self.feature_posts_4=ko.observable();


        //self.resorts = new Resorts();
        //self.meetups = new Meetups();
        // Methors
        self.viewChange = function (view, intent, useCache) {
            var search_zip=self.search_zip();
            console.log(view);
            if (!useCache || !vms[view]) {
                vms[view] = new views[view](self);
            }
            self.view(view);
            self.view(view);
            if ( !! intent) {
                vms[view].intent(intent);
            };
            self.VM(vms[view]);
            if(view=='event'){
                location.hash = view+'/'+intent.id;
            }
            else if (view=='conversation_page'){
                location.hash = 'conversation_page='+intent.post_id+'='+intent.asker_id;
            }                
            else if (view=='search' && ( !!search_zip)){
                location.hash = 'search_zip='+search_zip;
            }                   
            else if (view=='search' && (!!intent)){
                self.search_zip(intent.search_zip);
                location.hash = 'search_zip='+intent.search_zip;
            }
            else{    
            location.hash = view;
            }
        }
        self.post_event = function () {
            self.viewChange('post');
        }
        self.notice = function () {
            self.viewChange('notice_page');
        }
        self.conversation = function () {
            self.viewChange('conversation_page');
        }
        self.login = function () {
            self.viewChange('login');
        }        
        self.search_result = function () {
            self.viewChange('search');
        }        
        self.back = function () {
            window.history.go(-1)
        };
        self.get_feature_post= function(){
                ajaxCall.get_feature_post().done(function (raw) {
                    //console.log(raw);
                    //self.feature_posts(raw);
                    self.feature_posts_0(raw[0]);
                    self.feature_posts_1(raw[1]);
                    self.feature_posts_2(raw[2]);
                    self.feature_posts_3(raw[3]);
                    self.feature_posts_4(raw[4]);
                   
                    
                });            
        };
        self.click_poll = function (poll) {
            self.viewChange('event', {
                id: poll.pk
            });
        };
        // init
        self.user.checkLogin();
        self.get_feature_post();
        //$.when(
        //    self.resorts.get(),
        //    self.meetups.get()
        //).done(function () {
        //    self.viewChange('search');
        //});
//        if(document.location.hostname=="127.0.0.1")
//            self.viewChange('main');
//        else
//            self.viewChange('main');
        //self.viewChange('search');
        
            // Client-side routes    
app.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'html/main.html',
        controller: 'ctrl_main'
      }).    
      when('/search', {
        templateUrl: 'html/search.html',
        controller: 'ctrl_search'
      }).
      when('/post', {
        templateUrl: 'html/post.html',
        controller: 'ctrl_post'
      }).    
      when('/login', {
        templateUrl: 'html/login.html',
        controller: 'ctrl_login'
      }).   
      when('/event/:id', {
        templateUrl: 'html/event.html',
        controller: 'ctrl_event'
      }).   
      when('/create_account', {
        templateUrl: 'html/create_account.html',
        controller: 'ctrl_create_account'
      }).   
      when('/notice_page', {
        templateUrl: 'html/notice_page.html',
        controller: 'ctrl_notice_page'
      }).   
      when('/conversation_page=:post_id=:asker_id', {
        templateUrl: 'html/conversation_page.html',
        controller: 'ctrl_conversation_page'
      }).   
      otherwise({
        redirectTo: '/'
      });
  }]);        
        
  
  
    }

    // LAUNCH


 
//ko.bindingHandlers.slider = {
//  init: function (element, valueAccessor, allBindingsAccessor) {
//    var options = allBindingsAccessor().sliderOptions || {};
//    $(element).slider(options);
//    ko.utils.registerEventHandler(element, "slidechange", function (event, ui) {
//        var observable = valueAccessor();
//        observable(ui.value);
//    });
//    ko.utils.domNodeDisposal.addDisposeCallback(element, function () {
//        $(element).slider("destroy");
//    });
//    ko.utils.registerEventHandler(element, "slide", function (event, ui) {
//        var observable = valueAccessor();
//        observable(ui.value);
//    });
//  },
//  update: function (element, valueAccessor) {
//    var value = ko.utils.unwrapObservable(valueAccessor());
//    if (isNaN(value)) value = 0;
//    $(element).slider("value", value);
//  }
//};

});
