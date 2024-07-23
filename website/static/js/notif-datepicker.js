const notif_picker = new Litepicker({
  element: document.getElementById("filter_date_notif"),
  singleMode: false,
  numberOfMonths: 2,
  plugins: ["ranges", "resetButton"],
  resetButton: true,
});
