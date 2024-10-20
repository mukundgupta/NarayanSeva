
window.onload = function () {
  
  // Get the value from localStorage
  var value = localStorage.getItem('Name');
        
  // Display the value on the page
  var output = document.getElementById('nameF-out');
  output.innerHTML = value;

  var tech_time = localStorage.getItem('time');
  var time_out = document.getElementById('tech-time-out');
  time_out.innerHTML = tech_time;


  
  
};

