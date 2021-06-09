function formatAndDisableDates(date) {
    const string = jQuery.datepicker.formatDate('yy-mm-dd', date);
    return [bookedDays.indexOf(string) == -1];
}

$(document).ready(function () {
    $(".bookingDatepicker").datepicker({
        minDate: new Date(opensAt),
        maxDate: new Date(closesAt),
        dateFormat: "dd.mm.yy",
        beforeShowDay: formatAndDisableDates,
    });
});