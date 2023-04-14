$(document).ready(function() {
    // Get the transaction details from the server and display them in the table
    $.get('/api/transactions/', function(data) {
      var transactionsTable = $('#transactions-table');
      for (var i = 0; i < data.length; i++) {
        var transaction = data[i];
        var row = '<tr><td>' + transaction.date + '</td>' +
                  '<td>' + transaction.description + '</td>' +
                  '<td>' + transaction.amount + '</td>' +
                  '<td>' + transaction.category + '</td>' +
                  '<td>' + transaction.payment_method + '</td>' +
                  '<td>' + transaction.reference_number + '</td>' +
                  '<td>' + transaction.status + '</td></tr>';
        transactionsTable.append(row);
      }
    });
  });
  

  