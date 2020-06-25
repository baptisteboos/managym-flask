/**
 * validateScoreColor takes one element and add css color:
 * green:  if elem >= 90(%)
 * yellow: if 80 <= elem < 90 
 * red:    if 80 > elem
 * @param selector - Jquery selector, one cell in our table
 */
function validateScoreColor(selector) {
  if (parseFloat($(selector).text()) >= 90) {
    $(selector).css('color', 'green').css('font-weight', 'bold');
  } else if (parseFloat($(selector).text()) < 80) {
    $(selector).css('color', 'red').css('font-weight', 'bold');
  } else {
    $(selector).css('color', '#b9b226').css('font-weight', 'bold');
  }
}

function handlerTargetResults (selector, init=false) { 
  if (!$(selector).text().match(/^[0-9]*\.?[0-9]*$/)) {
  $(selector).text('0');
  }

  // Convert number from cells in float
  var row = $(selector).parent();
  var tsv = parseFloat($(row).children('.tsv').text());   // target_start_value
  var tex = parseFloat($(row).children('.tex').text());   // target_execution
  var rsv = parseFloat($(row).children('.rsv').text());   // result_start_value
  var rex = parseFloat($(row).children('.rex').text());   // result_execution 

  // -- Calcultate empties cells --
  // target total
  $(row).children('.ttot').text(String((tsv + tex).toFixed(2))); 

  // target result start value (in %)
  $(row).children('.trsv').text(String((tsv != 0 ? rsv / tsv * 100 : 0).toFixed(2)));
  validateScoreColor($(row).children('.trsv'))

  // target result executive (in %)
  $(row).children('.trex').text(String((tex != 0 ? rex / tex * 100 : 0).toFixed(2)));
  validateScoreColor($(row).children('.trex'))

  // result total
  $(row).children('.rtot').text(String((rsv + rex).toFixed(2)));

  // target result total (in %)
  $(row).children('.trtot').text(String(((tsv+tex) != 0 ? (rsv + rex) / (tsv + tex) * 100 : 0).toFixed(2)));
  validateScoreColor($(row).children('.trtot'))


  // --- Total result event (last line) ---
  var tbody = $(selector).closest('tbody');

  /**
   * sumCells: add all the factors and show in a res
   * @param factors - Jquery selector of factors
   * @param res     - Jquery selector of res
   */
  function sumCells(factors, res) {
    let sum = 0;
    $(tbody).find(factors).each(function() {
      sum += parseFloat( $(this).text() );
    });
    $(tbody).find(res).text(String(sum.toFixed(2)));
  }

  /**
   * ratioPercentage: calcultate numerator on denominator and show on a quotient
   *                  with colors with validateScoreColor
   * @param numerator   - Jquery selector of the numerator
   * @param denominator - Jquery selector of the denominator
   * @param quotient    - Jquery selector of the quotient
   */
  function ratioPercentage(numerator, denominator, quotient) {
    denominator = parseFloat($(tbody).find(denominator).text());
    numerator = parseFloat($(tbody).find(numerator).text());
    let ratio = denominator ? (numerator / denominator) * 100 : 0;
    $(tbody).find(quotient).text(String(ratio.toFixed(2)));
    validateScoreColor($(tbody).find(quotient));
  }

  // target start value total
  sumCells('td.tsv', 'td.tsvtot');
  // target executive total
  sumCells('td.tex', 'td.textot');
  // target total
  sumCells('td.ttot', 'td.target-total');
  // result start value total
  sumCells('td.rsv', 'td.rsvtot');
  // result executive total
  sumCells('td.rex', 'td.rextot');
  // result total
  sumCells('td.rtot', 'td.result-total');

  // ratio start value total (in %)
  ratioPercentage('td.rsvtot', 'td.tsvtot', 'td.trsvtot');
  // ratio executive total (in %)
  ratioPercentage('td.rextot', 'td.textot', 'td.trextot');
  // ration score total (in %)
  ratioPercentage('td.result-total', 'td.target-total', 'td.target-result-total');

  if (!init) {
    // Save new targets in database post form
    var url =  window.location.pathname + '/update_target';
    var event_id = $(selector).closest('.collapse').attr('id').slice(13);
    var apparatus_id = $(selector).parent().attr('class').split(' ')[1];
    var data = {event_id: event_id, apparatus_id: apparatus_id, tsv: tsv, tex: tex, rsv: rsv, rex: rex, target:parseFloat($(tbody).find('td.target-total').text()), result:parseFloat($(tbody).find('td.result-total').text())};
    $.post(url, data);
  }
}


$(document).ready(function() {
  // Start with target tab open on athlete profile
  $('#athlete-tabs a[href="#targets-content"]').tab('show')

  // Load the value of target/results table when click on button (no request)
  $('#accordionTargetResults button').on('click', evt => {
    var id_content = $(evt.target).attr('aria-controls');
    $('#'+id_content+'>.card-body tr.apparatus').each(function() {
      handlerTargetResults($(this).children('td[contenteditable]').first(), init=true);
    });
  });

  // Everytime we change a cell of the table we save it in db and recalculate the row
  $('tr.apparatus>td[contenteditable]').on('blur', evt => {
    handlerTargetResults($(evt.target));
  });
});
