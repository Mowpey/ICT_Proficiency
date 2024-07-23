const exam_picker = new Litepicker({
  element: document.getElementById("filter_date_exam"),
  singleMode: false,
  numberOfMonths: 2,
  plugins: ["ranges", "resetButton"],
  resetButton: true,
});
