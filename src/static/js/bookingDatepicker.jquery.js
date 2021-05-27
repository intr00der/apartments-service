
function DisableDates(date) {
    const string = jQuery.datepicker.formatDate('dd.mm.yy', date);
    return [booked_days.indexOf(string) == -1];
}

$(document).ready(function () {
    $(".bookingDatepicker").datepicker({
        minDate: new Date(opens_at),
        maxDate: new Date(closes_at),
        dateFormat: "dd.mm.yy",
        beforeShowDay: DisableDates,
    });
});