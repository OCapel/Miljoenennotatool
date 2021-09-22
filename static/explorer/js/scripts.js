
var frequencies = JSON.parse(document.getElementById('frequencies').innerText);


var layout = {
    title: 'Relevantie over tijd',
};

var trace2 = {
    type: "pie",
    values: Object.values(frequencies),
    labels: Object.keys(frequencies),

};


Plotly.newPlot('category_pie', [trace2], {title: 'Aantal hits per categorie'});


// function toggleSummary() {
//     var mapDiv = document.getElementById('summary');
//     if (mapDiv.style.display === 'none') {
//         mapDiv.style.display = 'block';
//         Plotly.relayout('relevance_ts', {autosize: true});
//         Plotly.relayout('category_pie', {autosize: true})
//     } else {
//         mapDiv.style.display = 'none';
//     }
// }
//
// function tableToggle(id) {
//     var state1 = document.getElementById('table-option1-' + id).checked;
//     var state2 = document.getElementById('table-option2-' + id).checked;
//
//     if (state1 && !state2) {
//         document.getElementById('table-text-' + id).style.display = '';
//         document.getElementById('table-img-' + id).style.display = 'none';
//     }
//     else if (!state1 && state2) {
//         document.getElementById('table-text-' + id).style.display = 'none';
//         document.getElementById('table-img-' + id).style.display = '';
//     }
// }