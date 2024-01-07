
// fetch all district list
$.get("/dashboard/get/district/all", function (data) {
    for (id in data) {
        $('#form-district').append(`<option value="${id}">${data[id]}</option>`);
    }
});

// fetch taluka list as per district
function get_taluka(district_id) {
    $('#form-taluka').html(`<option selected value="default" disabled>Select Taluka</option>`);

    $.get("/dashboard/get/taluka/all", { 'district-id': district_id }, function (data) {
        for (id in data) {
            $('#form-taluka').append(`<option value="${id}">${data[id]}</option>`);
        }
    });
}

// fetch Policestation list as per taluka
function get_policestation(taluka_id) {
    $('#form-policestation').html(`<option selected value="default" disabled>Select Police Station</option>`);

    $.get("/dashboard/get/policestation/all", { 'taluka-id': taluka_id }, function (data) {
        for (id in data) {
            $('#form-policestation').append(`<option value="${id}">${data[id]}</option>`);
        }
    });
}

// reset form selectionss
function form_reset() {
    $('#form-taluka').html(`<option selected value="default" disabled>Select Taluka</option>`);
    $('#form-policestation').html(`<option selected value="default" disabled>Select Police Station</option>`);
}