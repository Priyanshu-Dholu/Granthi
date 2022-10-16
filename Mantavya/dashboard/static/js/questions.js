// All Question's
const q11 = {
    1: "Through a person known to a police officer",
    2: "With a neighbour/ local leader",
    3: "On your own"
}
const q22 = {
    4: "More than 15 minutes",
    5: "15 minutes",
    6: "10 minutes",
    7: "5 minutes",
    8: "Immediately"
}
const q33 = {
    9: "Worst",
    10: "Bad",
    11: "Good",
    12: "V.Good",
    13: "Excellent"
}

// Update Question data
function updateData(data) {
    q1.data.datasets[0].data = Object.values(data['q1']['percentage']);
    q2.data.datasets[0].data = Object.values(data['q2']['percentage']);
    q3.data.datasets[0].data = Object.values(data['q3']['percentage']);
    chartUpdate();

    var i = 1;
    var j = 1;
    for (id in data) {
        $('#t' + id + ' tbody tr td:nth-child(2)').each(function () {
            if (data[id]['count'][i])
                $(this).text(addCommas(data[id]['count'][i]));
            else
                $(this).text(0);
            i++;
        });
        $('#t' + id + ' tbody tr td:nth-child(3)').each(function () {
            if (data[id]['percentage'][j])
                $(this).text(addCommas(String(data[id]['percentage'][j]).slice(0, 4)) + '%');
            else
                $(this).text('0%');
            j++;

        });
    }
}

class Question {

    policestation(request_data) {
        $.getJSON("/dashboard/get/question/ps", request_data, function (data) {
            updateData(data);
        });
    }

    taluka(request_data) {
        $.getJSON("/dashboard/get/question/tk", request_data, function (data) {
            updateData(data);
        });
    }

    district(request_data) {
        $.getJSON("/dashboard/get/question/dt", request_data, function (data) {
            updateData(data);
        });
    }

}