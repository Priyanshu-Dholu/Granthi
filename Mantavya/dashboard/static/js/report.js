// fetch and update feedbacks response table 

function updateTableData(data) {
    var i = 1;
    for (d in data) {
        $('#report-data').append(`<tr><th>${i}</th><td >${d}</td><td>${data[d]['date']}</td><td>${q11[data[d]['q1']]}</td><td>${q22[data[d]['q2']]}</td><td>${q33[data[d]['q3']]}</td><td>${data[d]['q4']}</td></tr>`);
        i++;
    }
}

class Report {
    policestation(request_data) {
        $.getJSON("/dashboard/get/policestation/report", request_data, function (data) {
            updateTableData(data)
        });
    }

    taluka(request_data) {
        $.getJSON("/dashboard/get/taluka/report", request_data, function (data) {
            updateTableData(data)
        });
    }

    district(request_data) {
        $.getJSON("/dashboard/get/district/report", request_data, function (data) {
            updateTableData(data)
        });
    }

}