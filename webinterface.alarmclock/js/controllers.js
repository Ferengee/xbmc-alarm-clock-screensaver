'use strict';

/* Controllers */

angular.module('alarmClock.controllers', [])
  .controller('AlarmClockController', ['$scope', 'xbmcRPC', function($scope, xbmcRPC) {
    var currentSong = {};
    var playlist = {items:[],
      OnClear: function(){
        this.items = [];
      },
      OnAdd:function(item){
        this.items.push(item);
      },
    }
    var player = {  
      OnPlay: function(data){
        xbmcRPC.getCurrentSong();
        //console.log("on play", data);
      },
      
      OnStop: function(data){
        updateSong({label:""});
        //console.log("on stop trigered", data);
      }
        
    };
    
    var clock = {
      date: new Date(),
      alarm: {minute: 0, hour: 0},
      UpdateClock: function(message){
        this.date = new Date(parseFloat(message.data) * 1000);
      },
      UpdateAlarm: function(message){
        console.log("UpdateAlarm:", message.respone);
      },
      update: function(){
        this.date = new Date();
        //console.log("beep");
      }
    };
    setInterval(function(){$scope.$apply(clock.update())},1000);
    
    this.Clock = clock;
    
    this.Playlist = playlist;
    this.Player = player;
    
    $scope.currentSong = currentSong;
    $scope.playlist = playlist;
    $scope.clock = clock;
    
    var updateSong = function(song){
      console.log("updatesong triggered");
      angular.forEach(song.item, function(value, key){
        currentSong[key] = value;
      });
    }
    
    this.setCurrentSong = function(song){
      updateSong(song);
      console.log("update:", song.item);
    }
        
    $scope.test = function(){
      console.log("ok")
      //xbmcRPC.getCurrentSong();
      xbmcRPC.getClock();
    }
    
    xbmcRPC.register(this);
  }])
  .controller('MyCtrl2', ['$scope', function($scope) {

  }]);
