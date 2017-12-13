//Shared javascript functions for subjects.

function goToSessionPrivate(sessionID) {
  $.ajax({
    data:{id : sessionID},
    type:"POST",
    url:REST + '/QuestionAnswered',
    headers: {
      'Access-Control-Allow-Origin': '*'
    },
    success: function(response) {
      AddSessionHistory(getCookie("Username"), sessionID);
      document.cookie="SessionID = " + sessionID + ";path=/";
      window.open(serverCWD + '/session.html', 'newwindow');
      //	window.location.href = "../session.html"
    },
    error: function(error){
      console.log(error);
    }
  })
}

function goToSessionPublic(sessionID) {
  $.ajax({
    data:{id : sessionID},
    type:"POST",
    url:REST + '/JoinSession',
    headers: {
      'Access-Control-Allow-Origin': '*'
    },
    success: function(response) {
      document.cookie="SessionID = " + sessionID + ";path=/";
      window.open('../session.html', 'newwindow');
      //  window.location.href = "../session.html"
    },
    error: function(error){
      console.log(error);
    }
  })
}

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("myTable");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "asc"; 
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.getElementsByTagName("TR");
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++;      
    } else {
      /*If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again.*/
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}

function AddSessionHistory(username, sessionID) {
    $.ajax({
        data:{username : username, question_id : sessionID},
        type:"POST",
        url: 'http://localhost:5000/AddSessionHistory',
        headers: {
            'Access-Control-Allow-Origin' : '*'
        },
        error: function(error) {
            console.log(error);
        } 
    })
}


  function getCookie(name) {
    var value = "; " + document.cookie;
      var parts = value.split("; " + name + "=");
      if (parts.length == 2) 
        return parts.pop().split(";").shift();
  }
