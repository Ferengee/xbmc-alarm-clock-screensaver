'use strict';

angular.module('alarmClock.services', [])
  .value('version', '0.1')
  .factory('xbmcRPC', ['$rootScope', function($scope) {
    var socket = new WebSocket("ws://"+window.location.hostname +":9090/jsonrpc");
    var controllers = [];
    
    var createCommand = function(id, method, parameters){
      var cmd = {"jsonrpc": "2.0", "method": "", "params": {}}
      cmd.method = method;
      if(id){ cmd.id = id; }
      if(parameters){ cmd.params = parameters }
      return cmd;
    }
    
    socket.onmessage = function(response){
      if(response.data){
        parseData(response.data);
      }
    }
    
    var notifyControllers = function(method, result){
      angular.forEach(controllers, function(controller){
        var path = method.split(".");
        var target = controller;
        var x;
        for (x = 0; x < path.length -1 ; x++){
          if(target[path[x]] !== undefined){
            target = target[path[x]];
          }
        }
        if(typeof(target[ path[x]]) == 'function'){
          target[ path[x]](result);
        }else {
          console.log("no: ",method, result);
        }
      });
    }
    
    var parseData = function(data){
      var answer = JSON.parse(data);
      if(answer.result){        
        $scope.$apply(notifyControllers(answer.id, answer.result));
      } else if(answer.method){
        $scope.$apply(notifyControllers(answer.method, answer.params)); 
      }else{
        //console.log("error:", data);
      }
      
    }
    
    var sendCmd = function(cmd){socket.send(JSON.stringify(cmd))}
    
    
    return {
      register: function(controller){
        controllers.push(controller);
      },
      getCurrentSong: function(){
        sendCmd(createCommand("setCurrentSong","Player.GetItem", 
          { "properties": ["title", "album", "artist", "duration", "thumbnail", "file", "fanart", "streamdetails"], "playerid": 0 }));
      },
      getClock: function(){
        sendCmd(createCommand(false, "Addons.ExecuteAddon", {"addonid": "webinterface.alarmclock", "params": {
            "method": "getClock"
        }}));   
      },
      setAlarm: function(hour, minute){
        sendCmd(createCommand("updateAlarm", "Addons.ExecuteAddon", {"addonid": "webinterface.alarmclock", "params": {
            "method": "setAlarm",
            "hour": hour,
            "minute": minute
        }}));   
      }
    };
  }]);