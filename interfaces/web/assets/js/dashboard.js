/* globals Chart:false, feather:false */

(function($) {
  $(document).ready(function() {
    'use strict'

    feather.replace()

    const wifiUrl = 'http://ubuntu.local/server/wifi';
    const wifiStatusUrl = 'http://ubuntu.local/server/wifi-status';
    const systemUrl = 'http://ubuntu.local/server/system';
    const logsUrl = 'http://ubuntu.local/server/logs';
    const eventsUrl = 'http://ubuntu.local/server/events';
    const intelligenceUrl = 'http://ubuntu.local/server/intelligence';

    $.getJSON(wifiStatusUrl, function (data) {
      var wifiStatusDiv = document.getElementById('wifistatus');
      if (data["access_point_mode"] == true){
        wifiStatusDiv.innerHTML += (
          '<p>' +
          'Status: <span data-feather="cloud-off" style="color:orange;">Access Point Mode</span><br><br>' +
          'You can access your Green Bot web interface by clicking on:<br> <a href="http://thegreenbot" style="color:green;">http://thegreenbot</a>' +
          '</p>'
        );
      } else {
        wifiStatusDiv.innerHTML += (
          '<p>' +
          'Status: <span data-feather="cloud" style="color:green;">Connected</span><br><br>' +
          'You can access your Green Bot web interface by clicking on:<br> <a href="http://thegreenbot" style="color:green;">http://thegreenbot</a>' +
          '</p>'
        );
      }
    });
  
    // Populate Logs
    $.getJSON(logsUrl, function (data) {
      $('#logsview').val(data);
    });

    $.getJSON(eventsUrl, function (data) {
      $('#eventsview').val(data);
    });

    // Populate System Info
    let sysInfo = $('#sysinfolist');

    $.getJSON(systemUrl, function (data) {
      data.forEach(function (item) {
        sysInfo.append($('<li>' + item + '</li>'));
      })
    });

  // Populate dropdown with list of Wifis
  let dropdown = $('#ssid');

  dropdown.empty();

  dropdown.append('<option selected="true" disabled>Choose Your Wifi Network</option>');
  dropdown.prop('selectedIndex', 0);
  $.getJSON(wifiUrl, function (data) {
    $.each(data, function (key, entry) {
      dropdown.append($('<option></option>').attr('value', entry).text(entry));
    })
  });

  $("#wifiForm").submit(function(e) {
    e.preventDefault();
  });

  function getFormDataInJson(form){
    var object = {};
    form.forEach((item) => {object[item.name] = item.value});
    return JSON.stringify(object);
  }


  $('#connectButton').click( function() {
    console.log('connectButton is clicked...')
    $.ajax({
        url: wifiUrl,
        type: 'post',
        dataType: 'json',
        data: getFormDataInJson($('form#wifiForm').serializeArray()),
        success: function(data) {
          console.log('Connecting to Wifi...')
        }
    });
  });

  $('#shutdownButton').click( function() {
    console.log('shutdownButton is clicked...')
    $.ajax({
        url: systemUrl,
        type: 'post',
        dataType: 'json',
        data: JSON.stringify({"command": "shutdown"}),
        success: function(data) {
          console.log('Shutting Down...')
        }
    });
  });


  $('#rebootButton').click( function() {
    console.log('rebootButton is clicked...')
    $.ajax({
        url: systemUrl,
        type: 'post',
        dataType: 'json',
        data: JSON.stringify({"command": "reboot"}),
        success: function(data) {
          console.log('Rebooting...')
        }
    });
  });


  $('#resetFactoryButton').click( function() {
    console.log('resetFactoryButton is clicked...')
    $.ajax({
        url: systemUrl,
        type: 'post',
        dataType: 'json',
        data: JSON.stringify({"command": "reset_factory"}),
        success: function(data) {
          console.log('Reset Factory...')
        }
    });
  });


  // Populate Intelligence Toggle Form
  $.getJSON(intelligenceUrl, function (data) {
    for (var item in data) {
      let toggle = $("#intelligence-" + item);
      if (data[item] == true) {
        toggle.bootstrapToggle('on');
      } else {
        toggle.bootstrapToggle('off');
      }
      
    }
  });

  $("#intelligenceForm").submit(function(e) {
    e.preventDefault();
  });



  function getToggleFormDataInJson(form){
    var object = {};
    form.forEach((item) => {object[item.name] = item.value});
    return JSON.stringify(object);
  }


  $('#intelligenceSaveButton').click( function() {
    console.log('intelligenceSaveButton is clicked...')
    $.ajax({
        url: intelligenceUrl,
        type: 'post',
        dataType: 'json',
        data: getToggleFormDataInJson($('form#intelligenceForm').serializeArray()),
        success: function(data) {
          console.log('Saving Intelligence Modules Configuration...')
        }
    });
  });


  });
})($);
